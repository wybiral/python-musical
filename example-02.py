import random

from musical.theory import Note, Scale
from musical.audio import effect, playback

from timeline import Hit, Timeline


# Define key and scale
key = Note('E3')
scale = Scale(key, 'harmonic minor')

time = 0.0 # Keep track of currect note placement time in seconds

timeline = Timeline()

note = key

# Semi-randomly queue notes from the scale
for i in xrange(64):
  if note.index > 50 or note.index < 24:
    # If note goes out of comfort zone, randomly place back at base octave
    note = scale.get(random.randrange(4) * 2)
    note = note.at_octave(key.octave)
  else:
    # Transpose the note by some small random interval
    note = scale.transpose(note, random.choice((-2, -1, 1, 2)))
  length = random.choice((0.125, 0.125, 0.25))
  timeline.add(time, Hit(note, length + 0.125))
  time += length

# Resolve
note = scale.transpose(key, random.choice((-1, 1, 4)))
timeline.add(time, Hit(note, 0.75))     # Tension
timeline.add(time + 0.5, Hit(key, 4.0)) # Resolution

print "Rendering audio..."

data = timeline.render()

print "Applying Chorus effect..."

data = effect.chorus(data, freq=3.14159)

# Reduce volume to 50%
data = data * 0.5

print "Playing audio..."

playback.play(data)

print "Done!"
