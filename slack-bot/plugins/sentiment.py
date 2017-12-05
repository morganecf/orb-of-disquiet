from __future__ import print_function
from __future__ import unicode_literals

import re
import json
import math
import socket
from termcolor import colored
from rtmbot.core import Plugin, Job


HOST = 'localhost'
RT_PORT = 9000
HUB_PORT = 9090
MAX_BYTES = 1024;

slack_credentials = json.load(open('../slack_credentials.json'))
bot_id = slack_credentials['zorg_bot_id']
hub_channel_id = slack_credentials['blushing_orb_id']
sentiment_channel_id = slack_credentials['orb_of_disquiet_id']

hub_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hub_socket.connect((HOST, HUB_PORT))

print('Connected to Hub prediction server')

rt_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rt_socket.connect((HOST, RT_PORT))

print('Connected to Rotten Tomatoes Sentiment prediction server')

class OrbPlugin(Plugin):
  erotic_emojis = [
    'vom',
    'cold_sweat',
    'neutral_face',
    'heart_eyes',
    'ahegao',
  ]

  sentiment_emojis = [
    'sob',
    'slightly_frowning_face',
    'neutral_face',
    'slightly_smiling_face',
    'grinning',
  ]

  @staticmethod
  def prediction_to_emoji(prediction, emojis):
    i = math.ceil(round(prediction) / 2)
    index = i - 1 if prediction >= 5 else i
    return emojis[index]

  @staticmethod
  def format_hub_score(prediction):
    return 'Sexiness: {:.2f} / 10'.format(prediction)

  @staticmethod
  def format_rt_score(prediction):
    return 'Sentiment: {:.2f} / 10'.format(prediction)

  def send_message(self, msg, channel, thread_ts=None):
    self.slack_client.api_call(
      'chat.postMessage',
      channel=channel,
      text=msg,
      username='zorgbot',
      thread_ts=thread_ts)

  def add_emoji(self, emoji, channel, ts):
    self.slack_client.api_call(
      'reactions.add',
      channel=channel,
      name=emoji,
      timestamp=ts)

  def print_text(self, text, pred):
    color = 'red' if pred > 5 else 'cyan'
    print(colored(text, color), '\t', pred)

  def clean_emojis(self, text):
    text = text.strip()
    emojis = re.findall(r'.*?(:\w+:)', text)
    for i, emoji in enumerate(emojis):
      cleaned = emoji.replace(':', '')
      cleaned = ' '.join(cleaned.split('_'))
      text = text.replace(emoji, cleaned)
    return text

  def process_message(self, data):
    channel = data['channel']
    is_right_channel = channel == hub_channel_id or channel == sentiment_channel_id
    is_bot = 'bot_id' in data or 'bot_id' in data.get('message', {})

    if is_right_channel and not is_bot:
      text = data.get('text')
      thread_id = data.get('ts')

      if text and thread_id:
        text = self.clean_emojis(text)
        message = str.encode(text + '\n')

        if channel == hub_channel_id:
          hub_socket.send(message)
          prediction = hub_socket.recv(MAX_BYTES)
          normalized = float(prediction.decode().strip()) * 10
          emoji_set = OrbPlugin.erotic_emojis
          output = OrbPlugin.format_hub_score(normalized)
        else:
          rt_socket.send(message)
          prediction = rt_socket.recv(MAX_BYTES)
          normalized = float(prediction.decode().strip()) * 2
          emoji_set = OrbPlugin.sentiment_emojis
          output = OrbPlugin.format_rt_score(normalized)

        emoji = OrbPlugin.prediction_to_emoji(normalized, emoji_set)
        self.send_message(output, channel, thread_ts=thread_id)
        self.add_emoji(emoji, channel, thread_id)
        self.print_text(text, normalized)
