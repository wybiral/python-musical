import numpy

from musical.theory import Note, Scale
from musical.audio import source, playback

# Define key and scale
key = Note('C4')
scale = Scale(key, 'major')

note = key
chunks = []
for i in xrange(len(scale)):
  third = scale.transpose(note, 2)
  chunks.append(source.sine(note, 0.5) + source.square(third, 0.5))
  note = scale.transpose(note, 1)
fifth = scale.transpose(key, 4)
chunks.append(source.sine(key, 1.5) + source.square(fifth, 1.5))

print "Rendering audio..."

data = numpy.concatenate(chunks)

# Reduce volume to 50%
data = data * 0.5

print "Playing audio..."

playback.play(data)

print "Done!"
