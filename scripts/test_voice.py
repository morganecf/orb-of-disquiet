import time
import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
  while True:
    try:
      audio = r.listen(source)
      text = r.recognize_google(audio)
      print(text)
    except sr.UnknownValueError:
      print('Unknown value')
      pass
