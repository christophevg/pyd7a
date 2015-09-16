# nop
# author: Christophe VG <contact@christophe.vg>

# class implementation of NoOperation

from d7a.alp.operations.operation import Operation

class NoOperation(Operation):
  def __init__(self):
    self.op     = 0
    self.operand_class = None
    super(NoOperation, self).__init__()
