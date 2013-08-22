import arbitrary
import jazz
from jazz import Describe, expect

@arbitrary.Values
class ArbitrarpyExampleTest(jazz.Describe):
  EMAIL = arbitrary.EMAIL
  PHONE = arbitrary.PHONE
  USERNAME = arbitrary.USER
  FIRST_NAME = arbitrary.NAME
  LAST_NAME = arbitrary.NAME
  ADDRESS = arbitrary.ADDR
  CITY = arbitrary.CITY
  STATE = arbitrary.STATE
  COUNTRY = arbitrary.COUNTRY
  ZIP = arbitrary.ZIP
  LAT = arbitrary.LAT
  LON = arbitrary.LON
  SENTENCE = arbitrary.SENTENCE
  PARAGRAPH = arbitrary.PARAGRAPH
  TAG = arbitrary.TAG
  ID = arbitrary.ID
  ID_STRING = arbitrary.HASH
  URL = arbitrary.URL
  DATE = arbitrary.DATE
  DATETIME = arbitrary.DATETIME
  NUMBER = arbitrary.NUMBER

if __name__ == '__main__':
  jazz.run()
