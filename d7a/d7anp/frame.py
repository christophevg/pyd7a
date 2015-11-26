
from d7a.support.schema import Validatable, Types
from d7a.d7anp.control import Control

class Frame(Validatable):

  SCHEMA = [{
    "control": Types.OBJECT(Control),
    "origin_access_id": Types.BYTES(), # TODO max size?
    "payload": Types.BYTES() # TODO max size?
  }]

  def __init__(self, control, origin_access_id, payload):
    self.control = control
    self.origin_access_id = origin_access_id
    self.payload = payload # TODO
    super(Frame, self).__init__()