# file
# author: Christophe VG <contact@christophe.vg>

# class implementations of File {*} Operands

import struct

from d7a.support.schema import Validatable, Types

class Offset(Validatable):
  
  SCHEMA = [
    {
      "id"    : Types.BYTE(),
      "size"  : Types.INTEGER([1]),
      "offset": Types.INTEGER(min=0, max=0xFF)
    },{
      "id"    : Types.BYTE(),
      "size"  : Types.INTEGER([2]),
      "offset": Types.INTEGER(min=0, max=0xFFFF)
    },{
      "id"    : Types.BYTE(),
      "size"  : Types.INTEGER([3]),
      "offset": Types.INTEGER(min=0, max=0xFFFFFF)
    },{
      "id"    : Types.BYTE(),
      "size"  : Types.INTEGER([4]),
      "offset": Types.INTEGER(min=0, max=0xFFFFFFFF)
    }
  ]
  
  def __init__(self, id=0, size=1, offset=0):
    self.id     = id
    self.size   = size
    self.offset = offset
    super(Offset, self).__init__()

  def __iter__(self):
    yield chr(self.id)
    
    byte = 0
    byte += (self.size - 1) << 6

    if self.size == 1:
      byte += self.offset
      yield byte
    else:
      offset = bytearray(struct.pack(">I", self.offset))
      if self.size == 2:   offset = offset[2:]
      elif self.size == 3: offset = offset[1:]
      
      byte += offset[0]
      yield byte
      for byte in offset[1:]: yield byte

class Data(Validatable):

  SCHEMA = [{
    "offset" : Types.OBJECT(Offset),
    "length" : Types.BYTE(),
    "data"   : Types.BYTES()
  }]
  
  def __init__(self, data=[], offset=Offset()):
    self.offset = offset
    self.data   = data
    super(Data, self).__init__()

  # for consistency with schema, e.g. if using generic attribute conversion, etc
  @property
  def length(self):
    return len(self.data)

  # the Python way ;-)
  def __len__(self):
    return self.length

  def __iter__(self):
    for byte in self.offset: yield byte
    yield chr(self.length)
    for byte in self.data: yield chr(byte)
