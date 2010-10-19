from scale import Scale

# TODO: Chord identification
# TODO: Extended and "added note" chords

class Chord:

  ''' Chord class handles multiple chord construction and manipulation
  '''

  def __init__(self, notes):
    self.notes = tuple(notes)

  def __repr__(self):
    return 'Chord(%s)' % repr(self.notes)

  def __len__(self):
    return len(self.notes)

  def __iter__(self):
    return iter(self.notes)

  def invert_up(self):
    ''' Invert chord up, shifting the lowest note up one octave
    '''
    notes = list(self.notes)
    index = notes.index(min(notes))
    notes[index] = notes[index].transpose(12)
    return Chord(notes)

  def invert_down(self):
    ''' Invert chord down, shifting the highest note down one octave
    '''
    notes = list(self.notes)
    index = notes.index(max(notes))
    notes[index] = notes[index].transpose(-12)
    return Chord(notes)

  @classmethod
  def fromscale(cls, root, scale):
    ''' Return chord of "root" within "scale"
    '''
    scale = Scale(root, scale)
    third = scale.transpose(root, 2)
    fifth = scale.transpose(root, 4)
    return cls((root, third, fifth))

  @classmethod
  def major(cls, root):
    ''' Return major triad
    '''
    return cls.fromscale(root, "major")

  @classmethod
  def minor(cls, root):
    ''' Return minor triad
    '''
    return cls.fromscale(root, "minor")

  @classmethod
  def augmented(cls, root):
    ''' Return augmented triad
    '''
    return cls.fromscale(root, "augmented")

  @classmethod
  def diminished(cls, root):
    ''' Return diminished triad
    '''
    return cls.fromscale(root, "diminished")

  @classmethod
  def progression(cls, scale, base_octave=3):
    ''' Return chord progression of scale instance as a list.
        Octave of tonic chord is at "base_octave"
    '''
    prog = []
    for root in scale:
      root = root.transpose(12 * base_octave)
      third = scale.transpose(root, 2)
      fifth = scale.transpose(root, 4)
      prog.append(cls((root, third, fifth)))
    return prog

