# schema.py
# author: Christophe VG <contact@christophe.vg>

# base class for schema-validatable entity classes

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
