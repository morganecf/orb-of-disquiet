import time
import socket

'''
Connects to simple Java prediction server to get a prediction on input text.
'''

HOST = 'localhost';
PORT = 9000;
MAX_BYTES = 1024;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print('Type a sentence to get sentiment.')

while True:
  text = input()
  message = str.encode(text + '\n')
  sock.send(message)
  pred = sock.recv(MAX_BYTES)
  print('Prediction:', pred.decode().strip())

  if text == 'STOP':
    print('Stopping client')
    break
