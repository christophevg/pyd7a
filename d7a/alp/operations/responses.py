# responses
# author: Christophe VG <contact@christophe.vg>

# class implementation of responses

from d7a.alp.operations.operation import Operation

from d7a.alp.regular_action       import RegularAction
from d7a.alp.operands.file        import Data, Offset

class ReturnFileData(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 32
    self.operand_class = Data
    super(ReturnFileData, self).__init__(*args, **kwargs)
