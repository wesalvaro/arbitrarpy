import math
import random
import sys

_LOWER_ALPHA = 'abcdefghijklmnopqrstuvwxyz'
_UPPER_ALPHA = _LOWER_ALPHA.upper()
_NUMBERS = '0123456789'
_WHITESPACES = ' \n\t\r'
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
      print 'Created arbitrary %s: %r' % (a, value)
      setattr(cls, a, value)
  return cls


class Arbitrary(object):
  """This class is a "mixin" to subclass for the test decorator."""


class Pattern(Arbitrary):

  def __init__(self, pattern):
    self.pattern = str(pattern)

  def Value(self):
    return Fill(self.pattern)

  def __mul__(self, v):
    return Pattern(self.pattern * v)

  def __add__(self, v):
    if isinstance(v, Arbitrary):
      pattern = v.pattern
    else:
      pattern = v
    return Pattern(self.pattern + pattern)

  def __getitem__(self, bounds):
    if bounds.start is not None and bounds.stop is not None:
      pattern_len = random.randrange(bounds.start, bounds.stop)
    elif bounds.start is not None:
      pattern_len = random.randrange(bounds.start, len(self.pattern))
    elif bounds.stop is not None:
      pattern_len = random.randrange(0, bounds.stop)
    else:
      pattern_len = len(self.pattern)
    if pattern_len > len(self.pattern):  # Extend pattern
      pattern = self.pattern * math.ceil(1. * pattern_len / len(self.pattern))
    else:
      pattern = self.pattern
    if bounds.step:  # Randomize
      pattern = ''.join(random.sample(self.pattern, pattern_len))
    else:
      pattern = self.pattern[:pattern_len]
    return Pattern(pattern)

class Float(Arbitrary):

  def __init__(self, start=None, stop=None):
    self.stop = sys.maxint if stop is None else stop
    self.start = -sys.maxint - 1 if start is None else start

  def Value(self):
    return random.uniform(self.start, self.stop)

  def __getitem__(self, bounds):
    assert type(bounds) == slice, 'Index must be a slice.'
    start = self.start if bounds.start is None else bounds.start
    stop = self.stop if bounds.stop is None else bounds.stop
    return Float(start=start, stop=stop)


class Range(Arbitrary):

  def __init__(self, start=None, stop=None, step=None):
    self.stop = sys.maxint if stop is None else stop
    self.start = -sys.maxint - 1 if start is None else start
    self.step = 1 if step is None else step

  def Value(self):
    return random.randrange(self.start, self.stop, step=self.step)
  
  def __getitem__(self, bounds):
    assert type(bounds) == slice, 'Index must be a slice.'
    start = self.start if bounds.start is None else bounds.start
    stop = self.stop if bounds.stop is None else bounds.stop
    step = self.step if bounds.step is None else bounds.step
    return Range(start=start, stop=stop, step=step)


class Index(Arbitrary):

  def __init__(self, items):
    self.items = items

  def Value(self):
    return self.items[random.randrange(0, len(self.items))]


ZIP = Pattern('#####')
WORD = Pattern('aaaaaaaa')
USER = Pattern('aaaa####')[6:8:True]
NAME = Pattern('Aaaaaaaa')
ADDR = Pattern('#### Aaaaaaaa AA')
PHONE = Pattern('(###) ###-####')
SSN = Pattern('###-##-####')
STATE = Index(['CA', 'TN', 'WA', 'FL', 'TX', 'NJ'])
INT = Range()
INT_POS = INT[0:]
INT_NEG = INT[:0]
FLOAT = Float()
