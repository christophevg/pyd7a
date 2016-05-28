from d7a.alp.action import Action
from d7a.alp.operations.nop import NoOperation
from d7a.alp.operations.operation import Operation
from d7a.support.schema import Types

__author__ = 'glenn'


class RegularAction(Action):
  SCHEMA = [{
    "group"    : Types.BOOLEAN(),
    "resp"     : Types.BOOLEAN(),
    "op"       : Types.BITS(6),
    "operation": Types.OBJECT(Operation),
    "operand"  : Types.OBJECT(nullable=True)  # there is no Operand base-class
  }]

  def __init__(self, group=False, resp=False, operation=NoOperation()):
    self.group     = group
    self.resp      = resp
    super(RegularAction, self).__init__(operation)

  def __iter__(self):
    byte = 0
    if self.group: byte |= 1 << 7
    if self.resp:  byte |= 1 << 6
    byte += self.op
    yield byte

    for byte in self.operation: yield byte

  def __str__(self):
    output = "op={}, operand={}({})".format(type(self.operation).__name__, type(self.operand).__name__, self.operand)
    return output