from d7a.sp.status import Status
from d7a.support.schema import Validatable, Types


class InterfaceStatusOperand(Validatable):

  SCHEMA = [{
    "interface_id"        : Types.BYTE(),
    "interface_status"    : Types.OBJECT(Status)
  }]

  def __init__(self, interface_id, interface_status):
    self.interface_id = interface_id
    self.interface_status   = interface_status
    super(InterfaceStatusOperand, self).__init__()
