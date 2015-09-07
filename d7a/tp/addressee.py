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

class Addressee(object):

  # constructor validates according to specification
  def __init__(self, ucast=False, vid=False, cl=0, id=None):
    self.ucast = ucast
    self.vid   = vid
    self.cl    = self.validate_cl(cl)
    self.id    = self.validate_id(id)

  def validate_cl(self, value):
    value = int(value)
    if value < 0x0 or value > 0xF:
      raise ValueError("Access Class must be within [0,0xF].")
    return value

  def validate_id(self, value):
    if self.id_length == 0 and value: 
      raise ValueError("can't set ID when length=0.")
    if self.id_length == 2 and (value < 0x0 or value > 0xFFFF):
      raise ValueError("ID with length=2 must be within [0,0xFFFF].")
    if self.id_length == 8 and (value < 0x0 or value > 0xFFFFFFFFFFFFFFFF):
      raise ValueError("ID with length=8 must be within [0,0xFFFFFFFFFFFFFFFF]")
    return value

  def validate(self):
    self.validate_cl(self.cl)
    self.validate_id(self.id)

  # model API

  @property
  def uses_unicast(self):
    return self.ucast

  @property
  def uses_broadcast(self):
    return not self.uses_unicast


  BROADCAST = 0
  VIRTUAL   = 1
  UNIVERSAL = 2 

  @property
  def id_type(self):
    if not self.ucast: return Addressee.BROADCAST
    if self.vid: return Addressee.VIRTUAL
    return Addressee.UNIVERSAL

  @property
  def has_virtual_id(self):
    return self.id_type == Addressee.VIRTUAL
  
  @property
  def has_universal_id(self):
    return self.id_type == Addressee.UNIVERSAL

  @property
  def id_length(self):
    return {
      Addressee.BROADCAST : 0,
      Addressee.VIRTUAL   : 2,
      Addressee.UNIVERSAL : 8
    }[self.id_type]
