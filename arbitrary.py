_LOWER_ALPHA = 'abcdefghijklmnopqrstuvwxyz'
_UPPER_ALPHA = _LOWER_ALPHA.upper()
_NUMBERS = '0123456789'
_WHITESPACES = '\n\t '
_SYMBOLS = r'`~!@#$%^&*(){}[]?+|/=\-_"<>,.\''
def Fill(pattern):
  """Fills an arbitrary pattern.

  Options:
    a: lower-case alpha characters
      'a' -> 'j', 'z', 'f'
    A: upper-case alpha characters
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
      4 lower-case letters or numbers
      followed by a single whitspace.
    '(4-9i)+?(4-9i)@(4-9a).?(2a).(2-3a)':
      This will look like an email address.
      aIUe+ibSTibasT@bxetstxbts.bx meets this pattern.
  """

def Values(cls):
  for a in cls.__dict__:
    if isinstance(getattr(cls, a), Arbitrary):
      setattr(cls, a, a.Value())
  return cls


class Arbitrary(object):
  PATTERN = ''

  def Value(self):
    return Fill(PATTERN)
    
