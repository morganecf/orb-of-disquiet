from __future__ import print_function
from __future__ import unicode_literals

import json
import math
import socket
from rtmbot.core import Plugin, Job

# TODO parse emojis

HOST = 'localhost'
RT_PORT = 9000
HUB_PORT = 9090
MAX_BYTES = 1024;

slack_credentials = json.load(open('../slack_credentials.json'))
bot_id = slack_credentials['zorg_bot_id']
channel_id = slack_credentials['zorg_testing_id']

hub_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hub_socket.connect((HOST, HUB_PORT))

print('Connected to Hub prediction server')

# rt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# rt_socket.connect((HOST, RT_PORT))

# print('Connected to Rotten Tomatoes Sentiment prediction server')

class OrbPlugin(Plugin):
  emojis = [
    'vom',
    'cold_sweat',
    'neutral_face',
    'heart_eyes',
    'ahegao',
  ]

  @staticmethod
  def prediction_to_emoji(prediction):
    i = math.ceil(round(prediction) / 2)
    index = i - 1 if prediction >= 5 else i
    return OrbPlugin.emojis[index]

  @staticmethod
  def format_output(prediction):
    return 'Sexiness: {:.2f} / 10'.format(prediction)

  def send_message(self, msg, thread_ts=None):
    self.slack_client.api_call(
      'chat.postMessage',
      channel=channel_id,
      text=msg,
      username='zorgbot',
      thread_ts=thread_ts)

  def add_emoji(self, emoji, ts):
    self.slack_client.api_call(
      'reactions.add',
      channel=channel_id,
      name=emoji,
      timestamp=ts)

  def process_message(self, data):
    is_right_channel = data['channel'] == channel_id
    is_bot = 'bot_id' in data or 'bot_id' in data.get('message', {})

    if is_right_channel and not is_bot:
      text = data.get('text')
      thread_id = data.get('ts')

      if text and thread_id:
        message = str.encode(text + '\n')
        hub_socket.send(message)
        prediction = hub_socket.recv(MAX_BYTES)
        normalized = float(prediction.decode().strip()) * 10
        output = OrbPlugin.format_output(normalized)
        emoji = OrbPlugin.prediction_to_emoji(normalized)
        self.send_message(output, thread_ts=thread_id)
        self.add_emoji(emoji, thread_id)
