# addressee
# author: Christophe VG <contact@christophe.vg>

# class implementation of addressee parameters

# D7ANP Addressee (Parameters)
#
# ADDC  1 byte:
#   b7-b6 RFU
#   b5    UCAST When set, the Addressee ID is present, and the message is
#               unicast, otherwise the message is broadcast
#   b4    VID   When set in combination with UCAST, the Addressee ID is virtual
#               (2 bytes), otherwise universal (8 bytes)
#   b3-b0 CL    Access Class of the Addressee
# ID    0/2/8 bytes ID of the Addressee

import struct

from d7a.support.schema import Validatable, Types

class Addressee(Validatable):
  
  # addressee ID length
  BROADCAST = 0
  VIRTUAL   = 2
  UNIVERSAL = 8
  
  SCHEMA = [
    {
      # broadcast
      "hasid"     : Types.BOOLEAN(),
      "vid"       : Types.BOOLEAN(),
      "cl"        : Types.BITS(4),
      "id_length" : Types.INTEGER([0]),
      "id"        : Types.INTEGER([None])
    },{
      # virtual
      "hasid"     : Types.BOOLEAN(True),
      "vid"       : Types.BOOLEAN(True),
      "cl"        : Types.BITS(4),
      "id_length" : Types.INTEGER([2]),
      "id"        : Types.INTEGER(min=0, max=0xFFFF)
    },{
      # unicast
      "hasid"     : Types.BOOLEAN(True),
      "vid"       : Types.BOOLEAN(False),
      "cl"        : Types.BITS(4),
      "id_length" : Types.INTEGER([8]),
      "id"        : Types.INTEGER(min=0, max=0xFFFFFFFFFFFFFFFF)
    }
  ]

  def __init__(self, cl=0, vid=False, id=None):
    self.hasid = id is not None
    self.vid   = vid
    self.cl    = cl
    self.id    = id
    super(Addressee, self).__init__()

  @property
  def id_length(self):
    return Addressee.length_for(hasid=self.hasid, vid=self.vid)

  @classmethod
  def length_for(self, hasid=False, vid=False):
    if not hasid: return Addressee.BROADCAST
    if hasid and vid: return Addressee.VIRTUAL
    return Addressee.UNIVERSAL

  def __iter__(self):
    byte = 0
    # pad 2 << 7 << 6
    if self.hasid: byte |= 1 << 5
    if self.vid:   byte |= 1 << 4
    byte += self.cl
    yield byte
    
    if self.id_length:
      id = bytearray(struct.pack(">Q", self.id))[8-self.id_length:]
      for byte in id: yield byte
