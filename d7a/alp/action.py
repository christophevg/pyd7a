# action
# author: Christophe VG <contact@christophe.vg>

# class implementation of action parameters

# D7A ALP Action 
#
# ALP Control   1 Byte
#   b7    GROUP Group this action with the next one (see 11.4.3)
#   b6    RESP  Return ALP Error Template
#   b5-b0 OP    Operation describing the action
# ALP Operand   N Bytes

from d7a.support.schema           import Validatable, Types

from d7a.alp.operations.operation import Operation
from d7a.alp.operations.nop       import NoOperation

class Action(Validatable):

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
    self.operation = operation
    super(Action, self).__init__()

  @property
  def op(self):
    return self.operation.op

  @property
  def operand(self):
    return self.operation.operand

  def __iter__(self):
    byte = 0
    if self.group: byte |= 1 << 7
    if self.resp:  byte |= 1 << 6
    byte += self.op
    yield byte
    
    for byte in self.operation: yield byte
