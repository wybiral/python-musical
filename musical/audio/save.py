import encode

# TODO: Support other formats and settings


def save_wave(data, path, rate=44100):
  ''' Save audio data to wave file, currently only 16bit
  '''
  import wave
  fp = wave.open(path, 'w')
  fp.setnchannels(1)
  fp.setframerate(rate)
  fp.setsampwidth(2)
  fp.setnframes(len(data))
  data = encode.as_int16(data)
  fp.writeframes(data.tostring())
  fp.close()

