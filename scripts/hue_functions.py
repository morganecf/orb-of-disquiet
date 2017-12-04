import sys
from phue import Bridge

# Transition times are specified in tenths of a second

COLORS = {
  'red': [0.6679, 0.3181],
  'yellow': [0.5425, 0.4196],
  'orange': [0.525, 0.385],
  'green': [0.41, 0.51721],
  'magenta': [0.4149, 0.1776],
  'blue': [0.1691, 0.0441],
  'white': [0.3, 0.3],
}

bridge = Bridge(sys.argv[1])
bridge.connect()

# Defaults are 1/10 of a second for 10 seconds
def flicker(start='magenta', end='blue', transition=0.1, duration=10):
  def flicker_once():
    bridge.set_light(1, 'xy', COLORS[start], transitiontime=transition * 10)
    time.sleep(transition)
    bridge.set_light(1, 'xy', COLORS[end], transitiontime=transition * 10)
    time.sleep(transition)

  num_iter = int(duration / transition)

  for _ in range(num_iter):
    flicker_once()

def pulse(color='red'):
  while True:
    bridge.set_light(1, 'xy', COLORS[color])
    bridge.set_light(1, 'bri', 10, transitiontime=10)
    time.sleep(1)
    bridge.set_light(1, 'bri', 80, transitiontime=10)
    time.sleep(1)

def heartbeat():
  while True:
    bridge.set_light(1, 'xy', COLORS['red'])
    bridge.set_light(1, 'bri', 10, transitiontime=0.5)
    time.sleep(0.5)
    bridge.set_light(1, 'bri', 80, transitiontime=10)
    time.sleep(1)

def fade_in(end=254, duration=5):
  bridge.set_light(1, 'bri', end, transitiontime=duration * 10)
  time.sleep(duration)

def fade_out(end=0, duration=5):
  bridge.set_light(1, 'bri', end, transitiontime=duration * 10)
  time.sleep(duration)

def off():
  bridge.set_light(1, 'bri', 0)

def on():
  bridge.set_light(1, 'xy', COLORS['white'])
  bridge.set_light(1, 'bri', 254)

def hue(color, duration=1):
  bridge.set_light(1, 'xy', COLORS[color], transitiontime=duration * 10)
  time.sleep(duration)

def test():
  off()
  hue('magenta', duration=0)
  fade_in(end=100, duration=2)
  flicker(transition=1, duration=2)
  fade_out(end=50, duration=2)
  # flicker(transition=0.1, duration=10)


# These don't seem to work right

def bpm(color='magenta', b=145):
  transition = 60 / b  # 0.4 seconds per beat
  bridge.set_light(1, 'xy', COLORS[color], transitiontime=transition * 10)
  time.sleep(transition)
  bridge.set_light(1, 'xy', COLORS['white'], transitiontime=0)
  time.sleep(transition)

def bpm2(color='magenta', b=145):
  transition = 60 / b / 2  # 0.4 seconds per beat
  bridge.set_light(1, 'xy', COLORS[color], transitiontime=transition * 10)
  time.sleep(transition)
  bridge.set_light(1, 'xy', COLORS['white'], transitiontime=transition * 10)
  time.sleep(transition)