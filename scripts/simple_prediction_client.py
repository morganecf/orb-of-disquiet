import time
import socket

'''
Connects to simple Java prediction server to get a prediction on input text.

NOTE: This is only working with python2.7 right now.
'''

HOST = 'localhost';
PORT = 9000;
MAX_BYTES = 1024;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print('Type a sentence to get sentiment.')

while True:
  text = raw_input()
  sock.send(text + '\n')
  pred = sock.recv(MAX_BYTES)
  print('Prediction:', pred)

  if text == 'STOP':
    print('Stopping client')
    break
