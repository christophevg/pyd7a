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

  def __iter__(self):
    yield self.interface_id
    for byte in self.interface_status: yield byte

  def __str__(self):
    return "interface-id={}, status={}".format(self.interface_id, self.interface_status)
