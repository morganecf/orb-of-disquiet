import time
import json
from slackclient import SlackClient

cred = json.load(open('../slack_credentials.json'))

sc = SlackClient(cred['token'])

if sc.rtm_connect():
  while True:
    msg = input('Type message:')
    sc.rtm_send_message(channel=cred['dm_id'], message=msg)
