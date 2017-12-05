import time
import json
import socket
from hue import Orb, scaler
from slackclient import SlackClient

'''
Connects to simple prediction server to get a prediction on incoming slack messages.
Changes the Hue bulb color to reflect sentiment.
'''

HUE_IP = '10.0.0.196'
HOST = 'localhost';
PORT = 9000;
MAX_BYTES = 1024;

orb = Orb(HUE_IP)
orb.connect()
orb.reset()

print('Connected to hue')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print('Connected to prediction server')

slack_credentials = json.load(open('../slack_credentials.json'))

# TODO replace with dedicated slack channel id
channel_id = slack_credentials['dm_id']

sc = SlackClient(slack_credentials['token'])
sc.rtm_connect()

print('Connected to Slack; polling...')

# Convert predictions on 0 - 5 scale to 0 - 1
to_unit_scale = scaler([0, 5], [-0.5, 1.5])

# Poll channel every second
while True:
  event = sc.rtm_read()

  # Make sure only getting messages from given channel
  if len(event) > 0 and event[0].get('channel') == channel_id:
    event = event[0]
    text = event.get('text')

    if text:
      # Send prediction to server
      text = ' '.join(text.splitlines())
      message = str.encode(text + '\n')
      sock.send(message)

      # Receive prediction
      pred = sock.recv(MAX_BYTES)
      pred = float(pred.decode().strip())
      unit_pred = to_unit_scale(pred)

      # Update hue (maintains a moving average)
      orb.emote(unit_pred)

      unicode_text = text.encode('utf-8')
      print(unicode_text, '------>', pred, unit_pred)

    time.sleep(1)
