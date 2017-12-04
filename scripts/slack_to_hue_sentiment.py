import json
import time
import datarobot as dr
from phue import Bridge
from slackclient import SlackClient

'''
Change Hue bulb color from blue to red based on sentiment of slack messages.

Also does some weird party strobe stuff.
'''

def scaler(input_range, output_domain):
  input_min, input_max = input_range
  output_min, output_max = output_domain
  def scale(x):
    return ((output_max - output_min) * (x - input_min) / (input_max - input_min)) + output_min
  return scale

# Color theory derived from graph here:
# https://developers.meethue.com/documentation/core-concepts

def blue_color(sentiment):
  # point 1: (0.15, 0.05)
  # point 2: (0.4, 0.5)
    # (0.5 - 0.05) / (0.4 - 0.15) = 1.8
    # y = 1.8x + b
    # 0.5 = 1.8 * 0.4 + b
    # b = 0.5 - 0.72 = -0.22
  # y = 1.8x - 0.22
  # We want to stay within the x color range of [0.15, 0.3]
  # And negative sentiment values will be between [0, 0.5)
  x = scaler([0, 0.4999], [0.15, 0.3])
  x_val = x(sentiment)
  y_val = 1.8 * x_val - 0.22
  return [x_val, y_val]

def red_color(sentiment):
  # y value stays constant at 0.35
  # We want to stay within the x color range of [0.4, 0.675]
  # And positive sentiment values will be between (0.5, 1]
  x = scaler([0.4999, 1], [0.4, 0.675])
  x_val = x(sentiment)
  return [x_val, 0.35]

# Convert sentiment [0 - 1] to chromacity [x, y]
def sentiment_to_chromacity(sentiment):
  if sentiment == 0.5:
    return [0.4, 0.3]
  if sentiment > 0.5:
    return red_color(sentiment)
  return blue_color(sentiment)

def party_strobe(bridge):
  bridge.set_light(1, 'xy', COLORS['magenta'], transitiontime=1)
  bridge.set_light(1, 'xy', COLORS['blue'], transitiontime=1)

# Common colors
COLORS = {
  'red': [0.6679, 0.3181],
  'yellow': [0.5425, 0.4196],
  'orange': [0.525, 0.385],
  'green': [0.41, 0.51721],
  'magenta': [0.4149, 0.1776],
  'blue': [0.1691, 0.0441],
  'white': [0.3, 0.3],
}

# Maximum number of seconds to wait for prediction job to finish
MAX_WAIT = 60 * 60

# Number of messags to predict in batches
MAX_MESSAGES = 5

# Tokens / credentials
dr_api_token = open('../dr_api_token').read().strip()
dr_ids = json.load(open('../sentiment_model_ids.json'))
project_id = dr_ids['dr_project']
model_id = dr_ids['dr_glm_sentiment_model']
slack_credentials = json.load(open('../slack_credentials.json'))
# zorg_id = slack_credentials['zorg_testing_id']
daniel_id = slack_credentials['dm_id']

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
bridge.set_light(1, 'xy', [0.3, 0.3])

# Keep track of all sentiments for rolling average
sentiments = []

# ugh this logic is getting involved
party_mode = False

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
      if text.startswith('[color]'):
        color = text.split(']')[1].strip()
        chromacity = COLORS.get(color, COLORS['white'])
        bridge.set_light(1, 'xy', chromacity, transitiontime=10)
      elif text.startswith('[partymode] on'):
        party_mode = True
        party_strobe(bridge)
        continue
      elif text.startswith('[partymode] off'):
        party_mode = False
        bridge.set_light(1, 'xy', COLORS['white'], transitiontime=10)
      else:
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
      avg_sentiment = predictions.positive_probability.mean()
      sentiments.append(avg_sentiment)
      avg_rolling_sentiment = sum(sentiments) / len(sentiments)
      print('Average Sentiment:', avg_sentiment)
      print('Average Rolling Sentiment:', avg_rolling_sentiment, 'across', len(sentiments) * MAX_MESSAGES, 'messages')
      # for i, row in enumerate(predictions.iterrows()):
      #     print('\t', messages[i], '\t---->\t', row[1].positive_probability)
      # print()

      # Modify Hue color
      chromacity = sentiment_to_chromacity(avg_rolling_sentiment)
      print('Chromacity:', chromacity)
      bridge.set_light(1, 'xy', chromacity, transitiontime=5)

      # Clear batch
      messages = []

    time.sleep(1)
