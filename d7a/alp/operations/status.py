from d7a.alp.operands.flush_result_status import FlushResultStatusOperand
from d7a.alp.operands.interface_status import InterfaceStatusOperand
from d7a.alp.operations.operation import Operation


class InterfaceStatus(Operation):
  def __init__(self, operand):
    self.op     = 34 # NOTE: 34 is shared with different status types depending on status operand extension bits
    self.operand_class = InterfaceStatusOperand
    super(InterfaceStatus, self).__init__(operand=operand)


# TODO not defined in spec yet, propose for inclusion
class FlushResultStatus(Operation):
  def __init__(self, operand):
    self.op = 34  # NOTE: 34 is shared with different status types depending on status operand extension bits
    self.operand_class = FlushResultStatusOperand
    super(FlushResultStatus, self).__init__(operand=operand)