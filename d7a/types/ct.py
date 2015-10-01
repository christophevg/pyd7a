# ct.py
# author: Christophe VG <contact@christophe.vg>

# class for representing compressed time

# The compressed time format allows compressing to 1 byte a time duration ranged
# from 0 to 507904 Ti (0 to 496 s) with variable Ti resolution. It can be 
# converted to Ti using the following formula: T = (4^EXP)x(MANT) Ti

import math

from cerberus import Validator

# Compressed Time
#
# b7-b5 EXP   Exponent (ranging from 0 to 7)
# b4-b0 MANT  Mantissa (ranging from 0 to 31)

from d7a.support.schema import Validatable
  
class CT(Validatable):
  
  SCHEMA = [{
    "exp"  : { "type": "integer", "min" : 0, "max":  7 },
    "mant" : { "type": "integer", "min" : 0, "max": 31 }
  }]

  def __init__(self, exp=0, mant=0):
    self.exp  = exp
    self.mant = mant
    super(CT, self).__init__()

  def __int__(self):
    return int(math.pow(4, self.exp) * self.mant)

  def __iter__(self):
    byte = 0
    byte |= self.exp << 5
    byte += self.mant
    yield byte
