import time
import json
import socket
from slackclient import SlackClient

'''
Connects to simple prediction server to get a prediction on incoming slack messages.
'''

HOST = 'localhost';
PORT = 9000;
MAX_BYTES = 1024;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print('Connected to prediction server')

slack_credentials = json.load(open('../slack_credentials.json'))

# TODO replace with dedicated slack channel id
channel_id = slack_credentials['dm_id']

sc = SlackClient(slack_credentials['token'])
sc.rtm_connect()

print('Connected to Slack; polling...')

# Poll channel every second
while True:
  event = sc.rtm_read()

  # Make sure only getting messages from given channel
  if len(event) > 0 and event[0].get('channel') == channel_id:
    event = event[0]
    text = event.get('text')

    # Send prediction to server
    if text:
      text = ' '.join(text.splitlines())
      message = str.encode(text + '\n')
      sock.send(message)
      pred = sock.recv(MAX_BYTES)
      print(text, '------>', pred.decode().strip())

    time.sleep(1)
