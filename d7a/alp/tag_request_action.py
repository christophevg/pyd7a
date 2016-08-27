from d7a.alp.action import Action
from d7a.alp.operations.nop import NoOperation
from d7a.alp.operations.operation import Operation
from d7a.support.schema import Types

class TagRequestAction(Action):
  SCHEMA = [{
    "respond_when_completed"    : Types.BOOLEAN(),
    "op"       : Types.BITS(6),
    "operation": Types.OBJECT(Operation),
    "operand"  : Types.OBJECT(nullable=True)  # there is no Operand base-class
  }]

  def __init__(self, respond_when_completed=True, operation=NoOperation()):
    self.respond_when_completed = respond_when_completed
    super(TagRequestAction, self).__init__(operation)

  def __iter__(self):
    byte = 0
    if self.respond_when_completed: byte |= 1 << 7
    byte += self.op
    yield byte

    for byte in self.operation: yield byte
