
from d7a.alp.operations.operation import Operation
from d7a.alp.operands.file        import DataRequest

class RequestFileData(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 1
    self.operand_class = DataRequest
    super(RequestFileData, self).__init__(*args, **kwargs)

