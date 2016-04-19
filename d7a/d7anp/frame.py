
from d7a.support.schema import Validatable, Types
from d7a.d7anp.control import Control
from d7a.d7atp.frame import Frame as D7atpFrame
from d7a.types.ct import CT

class Frame(Validatable):

  SCHEMA = [{
    "timeout": Types.OBJECT(CT),
    "control": Types.OBJECT(Control),
    "origin_access_id": Types.BYTES(), # TODO refactor to use OriginAddressee (subclass of addressee containing control and access_id)
    "d7atp_frame": Types.OBJECT(D7atpFrame)
  }]

  def __init__(self, timeout, control, origin_access_id, d7atp_frame):
    self.timeout = timeout
    self.control = control
    self.origin_access_id = origin_access_id
    self.d7atp_frame = d7atp_frame # TODO
    super(Frame, self).__init__()