from collections import deque
import math
import random
import numpy
from scipy.signal import waveforms

def silence(length, rate=44100):
  ''' Generate 'length' seconds of silence at 'rate'
  '''
  return numpy.zeros(int(length * rate))


def pygamesound(sound):
  ''' Create numpy array from pygame sound object
      rate is determined by pygame.mixer settings
  '''
  import pygame
  pygame.sndarray.use_arraytype('numpy')
  array = pygame.sndarray.array(sound)
  rate, format, channels = pygame.mixer.get_init()
  data = numpy.zeros(len(array))
  for i, sample in enumerate(array):
    data[i] = sum(sample)
  if format < 0:
    data /= (2 ** -format) / 2
  else:
    data = (data / (2 ** format)) * 2 - 1
  return data
  

def generate_wave_input(freq, length, rate=44100, phase=0.0):
  ''' Used by waveform generators to create frequency-scaled input array
  '''
  length = int(length * rate)
  phase *= float(rate) / 2
  factor = float(freq) * (math.pi * 2) / rate
  return (numpy.arange(length) + phase) * factor


def sine(freq, length, rate=44100, phase=0.0):
  ''' Generate sine wave for frequency of 'length' seconds long
      at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
      into the wave that it starts on.
  '''
  data = generate_wave_input(freq, length, rate, phase)
  return numpy.sin(data)


def sawtooth(freq, length, rate=44100, phase=0.0):
  ''' Generate sawtooth wave for frequency of 'length' seconds long
      at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
      into the wave that it starts on.
  '''
  data = generate_wave_input(freq, length, rate, phase)
  return waveforms.sawtooth(data)


def square(freq, length, rate=44100, phase=0.0):
  ''' Generate square wave for frequency of 'length' seconds long
      at a rate of 'rate'. The 'phase' of the wave is the percent (0.0 to 1.0)
      into the wave that it starts on.
  '''
  data = generate_wave_input(freq, length, rate, phase)
  return waveforms.square(data)


def ringbuffer(data, length, decay=1.0, rate=44100):
  ''' Repeat data for 'length' amount of time, smoothing to reduce higher
      frequency oscillation. decay is the percent of amplitude decrease.
  '''
  phase = len(data)
  length = int(rate * length)
  out = numpy.resize(data, length)
  for i in xrange(phase, length):
    index = i - phase
    out[i] = (out[index] + out[index + 1]) * 0.5 * decay
  return out


def pluck(freq, length, decay=0.998, rate=44100):
  ''' Create a pluck noise at freq by sending white noise through a ring buffer
      http://en.wikipedia.org/wiki/Karplus-Strong_algorithm
  '''
  freq = float(freq)
  phase = int(rate / freq)
  data = numpy.random.random(phase) * 2 - 1
  return ringbuffer(data, length, decay, rate)

