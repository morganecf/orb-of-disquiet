import sys
import time
import socket
from hue import Orb
from termcolor import colored

'''
Connects to simple Java prediction server to get a prediction on input text.
'''

try:
  port = int(sys.argv[1])
except IndexError:
  print('Using port 9000 (emotion)')
  port = 9000

HUE_IP = '192.168.0.30'
HOST = 'localhost';
MAX_BYTES = 1024;

orb = Orb(HUE_IP)
orb.connect()
orb.reset()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, port))

print('Type a sentence to get sentiment.')

while True:
  text = input()
  message = str.encode(text + '\n')
  sock.send(message)
  pred = sock.recv(MAX_BYTES)
  orb_input = float(pred.decode().strip())

  # for erotic it's 0 - 1, for emotion it's 1 - 5
  # hue expects 0 -1
  orb.emote(orb_input)
  # orb.emote(orb_input / 5)

  # color = 'red' if orb_input > 2.5 else 'blue'
  color = 'red' if orb_input > 0.5 else 'blue'
  print('\t', colored(str(orb_input), color))

  if text == 'STOP':
    print('Stopping client')
    break
