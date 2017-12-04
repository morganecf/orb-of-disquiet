import json
import time
import datarobot as dr
from phue import Bridge
from slackclient import SlackClient

'''
Prototype for Blushing Orb (responding to Slack message), but with very high-latency predictions.
'''

def scaler(input_range, output_domain):
  input_min, input_max = input_range
  output_min, output_max = output_domain
  def scale(x):
    return ((output_max - output_min) * (x - input_min) / (input_max - input_min)) + output_min
  return scale

def brightness(prediction):
  return scaler([0, 1], [0, 254])(prediction)

# Maximum number of seconds to wait for prediction job to finish
MAX_WAIT = 60 * 60

# Number of messages to predict in batches
MAX_MESSAGES = 3

# Tokens / credentials
dr_api_token = open('../dr_api_token').read().strip()
slack_credentials = json.load(open('../slack_credentials.json'))
daniel_id = slack_credentials['dm_id']

model_ids = json.load(open('../sentiment_model_ids.json'))
project_id = model_ids['hub_sentiment']['best_model_id']
model_id = model_ids['hub_sentiment']['project_id']

# Connect to DR
dr.Client(endpoint='https://app.datarobot.com/api/v2', token=dr_api_token)
project = dr.Project.get(project_id)
model = dr.Model.get(project_id, model_id)

# Connect to slack
sc = SlackClient(slack_credentials['token'])
sc.rtm_connect()

# Connect to Hue bridge
bridge = Bridge('10.0.0.196')
bridge.connect()

# Set to neutral
bridge.set_light(1, 'xy', [0.2, 0.1])
bridge.set_light(1, 'bri', 0)

print('Waiting for messages...')

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

      # Make batch predictions
      pred_dataset = project.upload_dataset('temp.csv')
      pred_job = model.request_predictions(pred_dataset.id)
      predictions = pred_job.get_result_when_complete()

      # Get average sentiment from last batch
      avg_prediction = predictions.positive_probability.mean()
      print('Measure of eroticism:', avg_prediction)

      # Modify hue color and intensity
      current = bridge.get_light(1)
      dx = 0.05 if avg_prediction > 0.5 else -0.05
      x = current['state']['xy'][0] + dx
      bri = brightness(avg_prediction)
      print('Setting:', x, bri)
      bridge.set_light(1, 'xy', [x, 0.1])
      bridge.set_light(1, 'bri', int(bri))

      print()

      # Clear batch
      messages = []

  time.sleep(1)
