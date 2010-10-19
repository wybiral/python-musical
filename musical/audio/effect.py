import source

# TODO: More effects. Distortion, echo, delay, reverb, phaser, pitch shift?
# TODO: Better generalize chorus/flanger (they share a lot of code)

def modulated_delay(data, modwave, dry, wet):
  ''' Use LFO "modwave" as a delay modulator (no feedback)
  '''
  out = data.copy()
  for i in xrange(len(data)):
    index = int(i - modwave[i])
    if index >= 0 and index < len(data):
      out[i] = data[i] * dry + data[index] * wet
  return out


def feedback_modulated_delay(data, modwave, dry, wet):
  ''' Use LFO "modwave" as a delay modulator (with feedback)
  '''
  out = data.copy()
  for i in xrange(len(data)):
    index = int(i - modwave[i])
    if index >= 0 and index < len(data):
      out[i] = out[i] * dry + out[index] * wet
  return out


def chorus(data, freq, dry=0.5, wet=0.5, depth=1.0, delay=25.0, rate=44100):
  ''' Chorus effect
      http://en.wikipedia.org/wiki/Chorus_effect
  '''
  length = float(len(data)) / rate
  mil = float(rate) / 1000
  delay *= mil
  depth *= mil
  modwave = (source.sine(freq, length) / 2 + 0.5) * depth + delay
  return modulated_delay(data, modwave, dry, wet)


def flanger(data, freq, dry=0.5, wet=0.5, depth=20.0, delay=1.0, rate=44100):
  ''' Flanger effect
      http://en.wikipedia.org/wiki/Flanging
  '''
  length = float(len(data)) / rate
  mil = float(rate) / 1000
  delay *= mil
  depth *= mil
  modwave = (source.sine(freq, length) / 2 + 0.5) * depth + delay
  return feedback_modulated_delay(data, modwave, dry, wet)


def tremolo(data, freq, dry=0.5, wet=0.5, rate=44100):
  ''' Tremolo effect
      http://en.wikipedia.org/wiki/Tremolo
  '''
  length = float(len(data)) / rate
  modwave = (source.sine(freq, length) / 2 + 0.5)
  return (data * dry) + ((data * modwave) * wet)

