from d7a.alp.operands.interface_status import InterfaceStatusOperand
from d7a.alp.operations.operation import Operation


class InterfaceStatus(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 51
    self.operand_class = InterfaceStatusOperand
    super(InterfaceStatus, self).__init__(*args, **kwargs)