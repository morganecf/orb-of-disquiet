import time
import socket
import speech_recognition as sr

'''
Connects to simple prediction server to get a prediction on incoming audio.
'''

HOST = 'localhost';
PORT = 9000;
MAX_BYTES = 1024;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

r = sr.Recognizer()

with sr.Microphone() as source:
  while True:
    try:
      audio = r.listen(source)
      text = r.recognize_google(audio)
      print('Predicting on:', text)
      message = str.encode(text + '\n')
      sock.send(message)
      pred = sock.recv(MAX_BYTES)
      print('\t------>', pred.decode().strip())
    except sr.UnknownValueError:
      print('Unknown value')
      pass
