import numpy


def as_uint8(data):
  ''' Return data encoded as unsigned 8 bit integer
  '''
  data = (data / 2 + 0.5).clip(0, 1)
  return (data * 255).astype(numpy.uint8)


def as_int8(data):
  ''' Return data encoded as signed 8 bit integer
  '''
  data = data.clip(-1, 1)
  return (data * 127).astype(numpy.int8)


def as_uint16(data):
  ''' Return data encoded as unsigned 16 bit integer
  '''
  data = (data / 2 + 0.5).clip(0, 1)
  return (data * 65535).astype(numpy.uint16)


def as_int16(data):
  ''' Return data encoded as signed 16 bit integer
  '''
  data = data.clip(-1, 1)
  return (data * 32767).astype(numpy.int16)
