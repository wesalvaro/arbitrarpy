import arbitrary
import jazz
from jazz import Describe, expect

@arbitrary.Values
class ArbitrarpyExampleTest(jazz.Describe):
  # EMAIL = arbitrary.EMAIL
  PHONE = arbitrary.PHONE
  USERNAME = arbitrary.USER
  FIRST_NAME = arbitrary.NAME
  LAST_NAME = arbitrary.NAME
  SSN = arbitrary.SSN
  ADDRESS = arbitrary.ADDR
  # CITY = arbitrary.CITY
  STATE = arbitrary.STATE
  # COUNTRY = arbitrary.COUNTRY
  ZIP = arbitrary.ZIP
  # LAT = arbitrary.LAT
  # LON = arbitrary.LON
  # SENTENCE = arbitrary.SENTENCE
  # PARAGRAPH = arbitrary.PARAGRAPH
  # TAG = arbitrary.TAG
  # ID = arbitrary.ID
  # ID_STRING = arbitrary.HASH
  # URL = arbitrary.URL
  # DATE = arbitrary.DATE
  # DATETIME = arbitrary.DATETIME
  INT = arbitrary.INT
  FLOAT = arbitrary.FLOAT

  def it_should_create_an_int(self):
    expect(type(self.INT)).toBe(int)

  def it_should_create_a_float(self):
    expect(type(self.FLOAT)).toBe(float)

  def it_should_create_a_username(self):
    expect(type(self.USERNAME)).toBe(str)
    expect(self.USERNAME).notToContain(' ')

  def it_should_create_an_address(self):
    addr = self.ADDRESS.split(' ')
    expect(int(addr[0])).toBeGreaterThan(0)
    expect(len(addr[1])).toBeGreaterThan(0)

  def it_should_create_different_names(self):
    expect(self.FIRST_NAME).notToEqual(self.LAST_NAME)


if __name__ == '__main__':
  jazz.run()
