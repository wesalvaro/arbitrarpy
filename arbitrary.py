import random
import sys

_LOWER_ALPHA = 'abcdefghijklmnopqrstuvwxyz'
_UPPER_ALPHA = _LOWER_ALPHA.upper()
_NUMBERS = '0123456789'
_WHITESPACES = '\n\t '
_SYMBOLS = r'`~!@#$%^&*(){}[]?+|/=\-_"<>,.\''

_PATTERN_KEY = {
  'a': _LOWER_ALPHA,
  'A': _UPPER_ALPHA,
  '#': _NUMBERS,
  'w': _WHITESPACES,
  's': _SYMBOLS,
}
def Fill(pattern):
  """Fills an arbitrary pattern.

  Options:
    a: start-case alpha characters
      'a' -> 'j', 'z', 'f'
    A: stop-case alpha characters
      'A' -> 'K', 'T', 'R'
    i: case insensitive alpha characters
      'i' -> 't', 'C', 'v'
    #: numeric characters
      '#' -> '8', '2', '5'
    w: any kind of whitespace
      'w' -> '\n', '\t', ' '
    s: any symbol
      's' -> '!', '#', '*'
    !: literally
      's!' -> 's'
    ?: maybe
      's?' -> ' ', ''
    (x-yabc): a group of x to y characters
      x and y may be any number and a, b, and c
      represent any character type.

  Examples:
    '(4a#)w':
      4 start-case letters or numbers
      followed by a single whitspace.
    '(4-9i)+?(4-9i)@(4-9a).?(2a).(2-3a)':
      This will look like an email address.
      aIUe+ibSTibasT@bxetstxbts.bx meets this pattern.
  """
  final = []
  for c in pattern:
    if c in _PATTERN_KEY:
      final.append(random.choice(_PATTERN_KEY[c]))
    else:
      final.append(c)
  return ''.join(final)

def Values(cls):
  for a, v in cls.__dict__.iteritems():
    if isinstance(v, Arbitrary):
      value = v.Value()
      print 'Created arbitrary value %r' % value
      setattr(cls, a, value)
  return cls


class Arbitrary(object):
  PATTERN = None
  BOUNDED = False

  def __init__(self, pattern=None, bounded=False):
    self.pattern = pattern or self.PATTERN
    self.bounded = bounded or self.BOUNDED

  def Value(self):
    if self.pattern:
      return Fill(self.pattern)
  

class RangedArbitrary(Arbitrary):

  def __init__(self, start=None, stop=None, step=None):
    self.stop = sys.maxint if stop is None else stop
    self.start = -sys.maxint - 1 if start is None else start
    self.step = 1 if step is None else step

  def Value(self):
    return random.randrange(self.start, self.stop, step=self.step)
  
  def __getitem__(self, bounds):
    assert type(bounds) == slice, 'Index must be a slice.'
    d = self.__dict__.copy()
    d['start'] = self.start if bounds.start is None else bounds.start
    d['stop'] = self.stop if bounds.stop is None else bounds.stop
    d['step'] = self.step if bounds.step is None else bounds.step
    return self.__class__(**d)


class IndexedArbitrary(RangedArbitrary):
  ITEMS = None

  def __init__(self, items=None, start=None, stop=None, **kwargs):
    self.items = items or self.ITEMS
    start = start or 0
    stop = stop or len(items)
    super(IndexedArbitrary, self).__init__(start=start, stop=stop, **kwargs)
    

  def Value(self):
    i = super(IndexedArbitrary, self).Value()
    return self.items[i]
   

class FloatingArbitrary(RangedArbitrary):

  def Value(self):
    return random.uniform(self.start, self.stop)
    

ZIP = Arbitrary(pattern='#####')      
USER = Arbitrary(pattern='aaaaaaaa')
NAME = Arbitrary(pattern='Aaaaaaaa')
ADDR = Arbitrary(pattern='#### Aaaaaaaa AA')
PHONE = Arbitrary(pattern='(###) ###-####')
SSN = Arbitrary(pattern='###-##-####')
STATE = IndexedArbitrary(items=['CA', 'TN', 'WA', 'FL', 'TX', 'NJ'])
INT = RangedArbitrary()
INT_POS = INT[0:]
INT_NEG = INT[:0]
FLOAT = FloatingArbitrary()
