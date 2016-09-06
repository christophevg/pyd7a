from d7a.alp.action import Action
from d7a.alp.operations.nop import NoOperation
from d7a.alp.operations.operation import Operation
from d7a.support.schema import Types

class TagResponseAction(Action):
  SCHEMA = [{
    "error"    : Types.BOOLEAN(),
    "op"       : Types.BITS(6),
    "operation": Types.OBJECT(Operation),
    "operand"  : Types.OBJECT(nullable=True)  # there is no Operand base-class
  }]

  def __init__(self, error, operation=NoOperation()):
    self.error = error
    super(TagResponseAction, self).__init__(operation)

  def __iter__(self):
    byte = 0
    if self.error: byte |= 1 << 6
    byte += self.op
    yield byte

    for byte in self.operation: yield byte
