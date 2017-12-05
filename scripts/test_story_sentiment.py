import socket
from termcolor import colored

PORT = 9090
HOST = 'localhost';
MAX_BYTES = 1024;

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

story = open('../data/test_story2.txt').readlines()
out = open('../data/test_story_predictions.tsv', 'a')

for line in story:
  if len(line) > 5:
    sentences = line.split('.')
    for sentence in sentences:
      message = str.encode(sentence + '\n')
      sock.send(message)
      pred = sock.recv(MAX_BYTES)
      pred = float(pred.decode().strip())
      color = 'red' if pred > 0.5 else 'blue'
      output = 'Prediction: {}'.format(pred)

      print(sentence.strip(), '\t', colored(output, color))
      # print(colored(output, color))
      # print()

      out.write(sentence.strip() + '\t' + str(pred) + '\n')

out.close()
