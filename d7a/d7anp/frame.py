
from d7a.support.schema import Validatable, Types
from d7a.d7anp.control import Control
from d7a.d7atp.frame import Frame as D7atpFrame

class Frame(Validatable):

  SCHEMA = [{
    "control": Types.OBJECT(Control),
    "origin_access_id": Types.BYTES(), # TODO max size?
    "d7atp_frame": Types.OBJECT(D7atpFrame)
  }]

  def __init__(self, control, origin_access_id, d7atp_frame):
    self.control = control
    self.origin_access_id = origin_access_id
    self.d7atp_frame = d7atp_frame # TODO
    super(Frame, self).__init__()