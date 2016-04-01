from d7a.alp.operations.operation import Operation
from d7a.alp.operands.file        import Data

class WriteFileData(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 4
    self.operand_class = Data
    super(WriteFileData, self).__init__(*args, **kwargs)