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

  def __init__(self, ucast=False, vid=False, cl=0, id=None):
    self.ucast = ucast
    self.vid   = vid
    self.cl    = cl
    self.id    = id

  # low-level properties

  @property
  def ucast(self):
    return self._ucast
  
  @ucast.setter
  def ucast(self, value):
    self._ucast = bool(value)

  @property
  def vid(self):
    return self._vid

  @vid.setter
  def vid(self, value):
    self._vid = bool(value)

  @property
  def cl(self):
    return self._cl

  @cl.setter
  def cl(self, value):
    if value < 0x0 or value > 0xF:
      raise Exception("Access Class must be within [0,0xF].")

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self, value):
    if self.id_length == 0 and value: 
      raise Exception("can't set ID when length=0.")
    if self.id_length == 2 and (value < 0x0 or value > 0xFFFF):
      raise Exception("ID with length=2 must be within [0,0xFFFF].")
    if self.id_length == 8 and (value < 0x0 or value > 0xFFFFFFFFFFFFFFFF):
      raise Exception("ID with length=8 must be within [0,0xFFFFFFFFFFFFFFFF]")
    self._id = value

  # functional API

  def uses_unicast(self):
    return self.ucast

  def uses_broadcast(self):
    return not self.uses_unicast()

  def has_virtual_id(self):
    return self.vid

  BROADCAST = 0
  VIRTUAL   = 1
  UNIVERSAL = 2 

  @property
  def id_type(self):
    if self.uses_broadcast(): return Addressee.BROADCAST
    if self.has_virtual_id(): return Addressee.VIRTUAL
    return Addressee.UNIVERSAL

  @property
  def id_length(self):
    return {
      Addressee.BROADCAST : 0,
      Addressee.VIRTUAL   : 2,
      Addressee.UNIVERSAL : 8
    }[self.id_type]
