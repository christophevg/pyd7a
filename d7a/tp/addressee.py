# addressee
# author: Christophe VG <contact@christophe.vg>

# class implementation of addressee parameters

# D7ATP Addressee (Parameters)
#
# ADDC  1 byte:
#   b7-b6 RFU
#   b5    UCAST When set, the Addressee ID is present, and the message is
#               unicast, otherwise the message is broadcast
#   b4    VID   When set in combination with UCAST, the Addressee ID is virtual
#               (2 bytes), otherwise universal (8 bytes)
#   b3-b0 CL    Access Class of the Addressee
# ID    0/2/8 bytes ID of the Addressee

from d7a.support.schema import Validatable

class Addressee(Validatable):
  
  # addressee ID type
  BROADCAST = 0
  VIRTUAL   = 1
  UNIVERSAL = 2
  
  SCHEMA = [
    {
      # broadcast
      "ucast"     : { "type": "boolean", "allowed": [ False ] },
      "vid"       : { "type": "boolean" },
      "cl"        : { "type": "integer", "min": 0x0, "max": 0xF },
      "id_length" : { "type": "integer", "allowed": [ 0 ] },
      "id"        : { "type": "integer", "nullable": True, "allowed": [ None ] }
    },{
      # virtual
      "ucast"     : { "type": "boolean", "allowed": [ True ] },
      "vid"       : { "type": "boolean", "allowed": [ True ] },
      "cl"        : { "type": "integer", "min": 0x0, "max": 0xF },
      "id_length" : { "type": "integer", "allowed": [ 2 ] },
      "id"        : { "type": "integer", "nullable": False, "min":0, "max": 0xFFFF }
    },{
      # unicast
      "ucast"     : { "type": "boolean", "allowed": [ True ] },
      "vid"       : { "type": "boolean", "allowed": [ False ] },
      "cl"        : { "type": "integer", "min": 0x0, "max": 0xF },
      "id_length" : { "type": "integer", "allowed": [ 8 ] },
      "id"        : { "type": "integer", "nullable": False, "min":0, "max": 0xFFFFFFFFFFFFFF }
    }
  ]

  def __init__(self, ucast=False, vid=False, cl=0, id=None):
    self.ucast = ucast
    self.vid   = vid
    self.cl    = cl
    self.id    = id
    super(Addressee, self).__init__()

  @property
  def id_type(self):
    if not self.ucast: return Addressee.BROADCAST
    if self.vid: return Addressee.VIRTUAL
    return Addressee.UNIVERSAL
  
  @property
  def id_length(self):
    return {
      Addressee.BROADCAST : 0,
      Addressee.VIRTUAL   : 2,
      Addressee.UNIVERSAL : 8
    }[self.id_type]
