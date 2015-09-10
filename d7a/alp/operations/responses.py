# responses
# author: Christophe VG <contact@christophe.vg>

# class implementation of responses

from d7a.alp.operations.operation import Operation
from d7a.alp.operands.file        import Data

class ReturnFileData(Operation):
  def __init__(self, *args, **kwargs):
    self.OP      = 32
    self.OPERAND = Data
    super(ReturnFileData, self).__init__(*args, **kwargs)
