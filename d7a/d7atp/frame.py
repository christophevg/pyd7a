
from d7a.support.schema import Validatable, Types
from d7a.d7atp.control import Control
from d7a.types.ct import CT

class Frame(Validatable):

  SCHEMA = [{
    "control": Types.OBJECT(Control),
    "dialog_id": Types.INTEGER(min=0, max=255),
    "transaction_id": Types.INTEGER(min=0, max=255),
    "timeout_template": Types.OBJECT(CT, nullable=True),
    "ack_template": Types.OBJECT(nullable=True),
    "payload": Types.BYTES() # TODO max size?
  }]

  def __init__(self, control, dialog_id, transaction_id, timeout_template, ack_template, payload):
    self.control = control
    self.dialog_id = dialog_id
    self.transaction_id = transaction_id
    self.timeout_template = timeout_template
    self.ack_template = ack_template
    self.payload = payload # TODO
    super(Frame, self).__init__()