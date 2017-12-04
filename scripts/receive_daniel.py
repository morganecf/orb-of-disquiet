import time
import json
from termcolor import colored
from slackclient import SlackClient

cred = json.load(open('slack_credentials.json'))
sc = SlackClient(cred['token'])

user_map = {
  cred['daniel_id']: 'Scromblublu',
  cred['morg_id']: 'Morg',
}

if sc.rtm_connect():
  while True:
    event = sc.rtm_read()
    if len(event) > 0 and 'channel' in event[0] and event[0]['channel'] == cred['dm_id']:
      event = event[0]
      user = event.get('user')
      text = event.get('text')
      if user:
        print(user_map[user], end=': ')
        if text:
          color = 'white' if user == cred['morg_id'] else 'blue'
          print(colored(text, color))
        elif event.get('type') == 'user_typing':
          print('typing...')
        else:
          print('Unknown event:', event)
      else:
        if event.get('type') == 'im_marked':
          print(colored('\t\t\tMessage seen', 'green'))
        # else:
        #   print('Unknown event:', event)
    time.sleep(1)
