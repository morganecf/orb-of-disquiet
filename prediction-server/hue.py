import numpy as np
from phue import Bridge

''' Helper methods
Color theory derived from graph here: https://developers.meethue.com/documentation/core-concepts
'''

def scaler(input_range, output_domain):
  input_min, input_max = input_range
  output_min, output_max = output_domain
  def scale(x):
    return ((output_max - output_min) * (x - input_min) / (input_max - input_min)) + output_min
  return scale

def blue_color(sentiment):
  # We want to stay within the x color range of [0.15, 0.3]
  # And negative sentiment values will be between [0, 0.5)
  x = scaler([0, 0.4999], [0.15, 0.3])
  x_val = x(sentiment)
  y_val = 1.8 * x_val - 0.22
  return [x_val, y_val]

def red_color(sentiment):
  # y value stays constant at 0.35
  # We want to stay within the x color range of [0.4, 0.675]
  # And positive sentiment values will be between (0.5, 1]
  x = scaler([0.4999, 1], [0.4, 0.675])
  x_val = x(sentiment)
  return [x_val, 0.35]

def brightness(prediction):
  return scaler([0, 1], [0, 254])(prediction)

class Orb:

  COLORS = {
    'red': [0.6679, 0.3181],
    'yellow': [0.5425, 0.4196],
    'orange': [0.525, 0.385],
    'green': [0.41, 0.51721],
    'magenta': [0.4149, 0.1776],
    'blue': [0.1691, 0.0441],
    'white': [0.3, 0.3],
  }

  def __init__(self, ip, bulb_id=1):
    self.ip = ip
    self.id = bulb_id
    self.bridge = Bridge(self.ip)

    # Keeps track of moving average of sentiment across
    # short-term memory.
    self.sentiment_values = []

  def connect(self):
    self.bridge.connect()

  def set_color(self, xy, t=1):
    self.bridge.set_light(self.id, 'xy', xy, transitiontime=1)

  def set_brightness(self, bri):
    self.bridge.set_light(self.id, 'bri', int(bri))

  def strobe(self):
    self.set_color(Orb.color_xy('magenta'))
    self.set_color(Orb.color_xy('blue'))

  def blush(self):
    pass

  def emote(self, sentiment, use_average=True):
    self.sentiment_values.append(sentiment)
    self.avg_sentiment = np.average(self.sentiment_values)

    if len(self.sentiment_values) > 3:
      self.sentiment_values = []

    sentiment = self.avg_sentiment if use_average else sentiment

    if sentiment == 0.5:
      color = [0.4, 0.3]
    if sentiment > 0.5:
      color = red_color(sentiment)
    else:
      color = blue_color(sentiment)
    self.set_color(color)

  def reset(self):
    self.num_messages = 0
    self.total_sentiment = 0
    self.set_color(Orb.color_xy('white'))

  @staticmethod
  def color_xy(color_name):
    return Orb.COLORS.get(color_name)


# import time
# orb = Orb('10.0.0.196')
# orb.connect()
# orb.reset()
# time.sleep(2)
# while True:
#   orb.strobe()
