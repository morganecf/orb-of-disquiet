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
  port = 9000

HUE_IP = '192.168.2.29'
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
  # print('Prediction:', pred.decode().strip())

  orb_input = float(pred.decode().strip())

  orb.emote(orb_input)

  print('\t', colored(str(orb_input * 10)))

  if text == 'STOP':
    print('Stopping client')
    break
