class Note:

  ''' Note class handles note/octave object, transposition, and frequency
      calculation
  '''

  NOTES = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

  def __init__(self, note):
    ''' Instantiate note, examples:
        Note('C')      # C4 (middle C)
        Note(0)        # C at octave 0
        Note(1)        # C-sharp at octave 0
        Note(12)       # C at octave 0
        Note('C2')     # C at octave 2
        Note('Db')     # D-flat at octave 4
        Note('D#3')    # D-sharp at octave 3
        Note(('G', 5)) # G note at octave 5

    '''
    if isinstance(note, str):
      self.index = Note.index_from_string(note)
    elif isinstance(note, tuple):
      self.index = Note.index_from_string(note[0]) + 12 * note[1]
    elif isinstance(note, Note):
      self.index = note.index
    else:
      self.index = int(note)

  def __repr__(self):
    return "Note('%s%i')" % (self.note, self.octave)

  def __cmp__(self, other):
    return cmp(self.index, other.index)

  def __float__(self):
    return self.frequency()

  @property
  def note(self):
    ''' note name property
    '''
    return Note.NOTES[self.index % 12]

  @property
  def octave(self):
    ''' octave number property
    '''
    return int(self.index / 12)

  @classmethod
  def index_from_string(cls, note):
    ''' Get index number from note string
    '''
    octave = 4
    note = note.strip().lower()
    if note[-1].isdigit():
      note, octave = note[:-1], int(note[-1])
    if len(note) > 1:
      note = cls.normalize(note)
    return cls.NOTES.index(note) + 12 * octave

  @classmethod
  def normalize(cls, note):
    ''' Translate accidentals and normalize flats to sharps
        For example E#->F, F##->G, Db->C#
    '''
    index = cls.NOTES.index(note[0].lower())
    for accidental in note[1:]:
      if accidental == '#':
        index += 1
      elif accidental == 'b':
        index -= 1
    return cls.NOTES[index % 12]

  def at_octave(self, octave):
    ''' Return new instance of note at given octave
    '''
    return Note((self.index % 12) + 12 * octave)

  def transpose(self, halfsteps):
    ''' Return transposed note by halfstep delta
    '''
    return Note(self.index + halfsteps)

  def frequency(self):
    ''' Return frequency of note
    '''
    return 16.35159783128741 * 2.0 ** (float(self.index) / 12.0)

