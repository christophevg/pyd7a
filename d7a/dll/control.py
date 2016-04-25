from d7a.support.schema import Validatable, Types

class Control(Validatable):

  SCHEMA = [{
    "is_target_address_set": Types.BOOLEAN(),
    "is_target_address_vid": Types.BOOLEAN(),
    "eirp_index": Types.INTEGER(None, 0, 63)
  }]

  def __init__(self, is_target_address_set, is_target_address_vid, eirp_index=0):
    self.is_target_address_set = is_target_address_set
    self.is_target_address_vid = is_target_address_vid
    self.eirp_index = eirp_index
    super(Control, self).__init__()

  def __iter__(self):
    byte = 0
    if self.is_target_address_set: byte |= 1 << 7
    if self.is_target_address_vid:  byte |= 1 << 6
    byte += self.eirp_index
    yield byte
