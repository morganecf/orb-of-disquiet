import time
from phue import Bridge
import speech_recognition as sr

'''
Simple example of how hue bulb can respond to speech input.
'''

b = Bridge('10.0.0.196')
b.connect()

b.set_light(1, 'bri', 0)
b.set_light(1, 'xy', [0.2, 0.1])

r = sr.Recognizer()

with sr.Microphone() as source:
  while True:
      audio = r.listen(source)
      text = r.recognize_google(audio)
      if 'hello' in text:
        b.set_light(1, 'bri', 250, transitiontime=1)
      if 'goodbye' in text:
        b.set_light(1, 'bri', 0)
      time.sleep(1)
