# schema.py
# author: Christophe VG <contact@christophe.vg>

# base class for schema-validatable entity classes

import math

from cerberus import Validator

class Validatable(object):
  def __init__(self):
    self.validate()

  SCHEMA = []

  def validate(self):
    validator = Validator(
      { "item": { "oneof_schema" : self.SCHEMA, "type": "dict"} },
      allow_unknown=True
    )
    obj_dict = {}
    for attr in dir(self): obj_dict[attr] = getattr(self, attr)
    if not validator.validate({ "item" : obj_dict }):
      raise ValueError(validator.errors)

class Types(object):
  @staticmethod
  def BOOLEAN():
    return { "type": "boolean", "nullable": False }

  @staticmethod
  def BYTE():
    return { "type": "integer", "nullable": False, "min": 0, "max": 0xFF }

  @staticmethod
  def OBJECT():
    return {  "nullable": False }

  @staticmethod
  def INTEGER():
    return { "type": "integer", "nullable": False }

  @staticmethod
  def ENUM(values):
    e = { "type": "integer", "allowed" : values}
    if None in values: e["nullable"] = True
    return e

  @staticmethod
  def BITS(length, min=0x0, max=None):
    max = max if max is not None else math.pow(2, length)
    return { "type": "integer", "min": 0x0, "max": max }

  @staticmethod
  def restrict(schema, values):
    schema["allowed"] = values
    if None in values: schema["nullable"] = True
    return schema
