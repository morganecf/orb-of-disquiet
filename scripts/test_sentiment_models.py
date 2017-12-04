import json
import time
import datarobot as dr
from slackclient import SlackClient

'''
Tests all sentiment models against each other by making batch predictions on Slack message data.
'''

# Maximum number of seconds to wait for prediction job to finish
MAX_WAIT = 60 * 60

# Number of messags to predict in batches
MAX_MESSAGES = 2

# Tokens / credentials
dr_api_token = open('../dr_api_token').read().strip()
slack_credentials = json.load(open('../slack_credentials.json'))
daniel_id = slack_credentials['dm_id']

# DR models
models = json.load(open('../sentiment_model_ids.json'))

# Connect to DR
dr.Client(endpoint='https://app.datarobot.com/api/v2', token=dr_api_token)

for model_name, model in models.items():
  model['project'] = dr.Project.get(model['project_id'])
  model['model'] = dr.Model.get(model['project_id'], model['best_model_id'])

# Connect to slack
sc = SlackClient(slack_credentials['token'])
sc.rtm_connect()

print('Connected; waiting for messages...')

# Read incoming messages from testing channel
messages = []
while True:
  event = sc.rtm_read()
  if len(event) > 0 and event[0].get('channel') == daniel_id:
    # Aggregate messages in batches of 5
    event = event[0]
    text = event.get('text')
    if text:
      print('Message:', text)
      messages.append(text)

    if len(messages) == MAX_MESSAGES:
      # Write messages to file. DR only accepts files for predictions
      # which is going to introduce a hell of a lot of latency
      with open('temp.csv', 'w') as fp:
        fp.write('text\n')
        for message in messages:
          fp.write(message.replace(',', '') + '\n')

      print('Predicting sentiment on', MAX_MESSAGES, 'messages')

      # Make batch predictions for each model
      for model_name, model in models.items():
        pred_dataset = model['project'].upload_dataset('temp.csv')
        pred_job = model['model'].request_predictions(pred_dataset.id)
        predictions = pred_job.get_result_when_complete()

        if model_name == 'rotten_tomatoes_sentiment':
          print(model_name, 'sentiment (0 - 5):', predictions.prediction.mean())
        else:
          print(model_name, 'sentiment (0 - 1):', predictions.positive_probability.mean())

      # Clear batch
      messages = []

    time.sleep(1)
