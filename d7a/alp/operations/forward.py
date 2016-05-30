from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.alp.operations.operation import Operation


class Forward(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 50
    self.operand_class = InterfaceConfiguration
    super(Forward, self).__init__(*args, **kwargs)