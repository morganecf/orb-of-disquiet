import time
import json
import pandas as pd
from datetime import datetime
from slackclient import SlackClient

'''
Collect all Slack message history between me & D.
'''

cred = json.load(open('../slack_credentials.json'))
sc = SlackClient(cred['token'])

messages = []

def get_messages(history):
  messages.extend([[message['text'], float(message['ts'])] for message in history['messages']])

history = sc.api_call('im.history', channel=cred['dm_id'], count=100)
get_messages(history)

while history['has_more']:
  last = history['messages'][-1]['ts']
  history = sc.api_call('im.history', channel=cred['dm_id'], count=100, latest=last)

  get_messages(history)
  time.sleep(2)

  print(len(messages), 'messages', str(datetime.fromtimestamp(float(last))))

df = pd.DataFrame(messages)
df.to_csv('daniel_messages.csv')
