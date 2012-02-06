import numpy
import encode


def pygame_play(data, rate=44100):
  ''' Send audio array to pygame for playback
  '''
  import pygame
  pygame.mixer.init(rate, -16, 1, 1024)
  sound = pygame.sndarray.numpysnd.make_sound(encode.as_int16(data))
  length = sound.get_length()
  sound.play()
  pygame.time.wait(int(length * 1000))
  pygame.mixer.quit()


def pygame_supported():
  ''' Return True is pygame playback is supported
  '''
  try:
    import pygame
  except:
    return False
  return True


def oss_play(data, rate=44100):
  ''' Send audio array to oss for playback
  '''
  import ossaudiodev
  audio = ossaudiodev.open('/dev/audio','w')
  formats = audio.getfmts()
  if ossaudiodev.AFMT_S16_LE & formats:
    # Use 16 bit if available
    audio.setfmt(ossaudiodev.AFMT_S16_LE)
    data = encode.as_int16(data)
  elif ossaudiodev.AFMT_U8 & formats:
    # Otherwise use 8 bit
    audio.setfmt(ossaudiodev.AFMT_U8)
    data = encode.as_uint8(data)
  audio.speed(rate)
  while len(data):
    audio.write(data[:1024])
    data = data[1024:]
  audio.flush()
  audio.sync()
  audio.close()


def oss_supported():
  ''' Return True is oss playback is supported
  '''
  try:
    import ossaudiodev
  except:
    return False
  return True


def pyaudio_play(data, rate=44100):
  ''' Send audio array to pyaudio for playback
  '''
  import pyaudio
  p = pyaudio.PyAudio()
  stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=1)
  stream.write(data.astype(numpy.float32).tostring())
  stream.close()
  p.terminate()


def pyaudio_supported():
  ''' Return True is pyaudio playback is supported
  '''
  try:
    import pyaudio
  except:
    return False
  return True


def play(data, rate=44100):
  ''' Send audio to first available playback method
  '''
  if pygame_supported():
    return pygame_play(data, rate)
  elif oss_supported():
    return oss_play(data, rate)
  elif pyaudio_supported():
    return pyaudio_play(data, rate)
  else:
    raise Exception("No supported playback method found")
