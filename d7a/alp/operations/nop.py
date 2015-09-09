# nop
# author: Christophe VG <contact@christophe.vg>

# class implementation of NoOperation

from d7a.alp.operations.operation import Operation

class NoOperation(Operation):
  def __init__(self):
    self.OP      = 0
    self.OPERAND = None
    super(NoOperation, self).__init__()
