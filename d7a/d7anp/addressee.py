# addressee
# author: Christophe VG <contact@christophe.vg>

# class implementation of addressee parameters


import struct

from d7a.support.schema import Validatable, Types
class IdType(object):
  BCAST = 1
  UID   = 2
  VID   = 3
  ALL   = [ BCAST, UID, VID ]

  @staticmethod
  def SCHEMA():
    return { "type": "integer", "allowed" : IdType.ALL }

class Addressee(Validatable):
  
  # addressee ID length
  ID_LENGTH_BROADCAST = 0
  ID_LENGTH_VID   = 2
  ID_LENGTH_UID = 8

  SCHEMA = [
     {
       # broadcast
       "id_type"   : Types.INTEGER([IdType.BCAST]),
       "access_class"        : Types.BITS(4),
       "id_length" : Types.INTEGER([0]),
       "id"        : Types.INTEGER([None])
     },{
       # virtual
      "id_type"   : Types.INTEGER([IdType.VID]),
       "access_class"        : Types.BITS(4),
       "id_length" : Types.INTEGER([2]),
       "id"        : Types.INTEGER(min=0, max=0xFFFF)
     },{
       # unicast
      "id_type"   : Types.INTEGER([IdType.UID]),
       "access_class"        : Types.BITS(4),
       "id_length" : Types.INTEGER([8]),
       "id"        : Types.INTEGER(min=0, max=0xFFFFFFFFFFFFFFFF)
     }
   ]


#  SCHEMA = [
#    {
#      "id_type"   : Types.INTEGER(IdType.ALL),
#      "cl"        : Types.BITS(4),
#      "id_length" : Types.INTEGER([0, 2, 8]),
#      "id"        : Types.INTEGER(min=0, max=0xFFFFFFFFFFFFFFFF)
#    }
#  ]

  def __init__(self, access_class=0, id_type=IdType.BCAST, id=None):
    self.id_type = id_type
    self.access_class = access_class
    self.id = id
    super(Addressee, self).__init__()

  @property
  def id_length(self):
    return Addressee.length_for(id_type=self.id_type)

  @classmethod
  def length_for(self, id_type):
    if id_type == IdType.BCAST: return Addressee.ID_LENGTH_BROADCAST
    if id_type == IdType.VID: return Addressee.ID_LENGTH_VID
    if id_type == IdType.UID: return Addressee.ID_LENGTH_UID

  @staticmethod
  def parse(s):
    _     = s.read("pad:2")
    id_type = s.read("uint:2")
    cl    = s.read("uint:4")
    l     = Addressee.length_for(id_type)
    id    = s.read("uint:"+str(l*8)) if l > 0 else None
    return Addressee(id_type=id_type, access_class=cl, id=id)

  def __iter__(self):
    byte = 0
    # pad 2 << 7 << 6
    byte |= self.id_type << 4
    byte += self.access_class
    yield byte
    
    if self.id_length > 0:
      id = bytearray(struct.pack(">Q", self.id))[8-self.id_length:]
      for byte in id: yield byte
