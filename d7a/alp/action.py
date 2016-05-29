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
    "op"       : Types.BITS(6),
    "operation": Types.OBJECT(Operation),
    "operand"  : Types.OBJECT(nullable=True)  # there is no Operand base-class
  }]

  def __init__(self, operation=NoOperation()):
    self.operation = operation
    super(Action, self).__init__()

  @property
  def op(self):
    return self.operation.op

  @property
  def operand(self):
    return self.operation.operand

  def __str__(self):
    output = "op={}, operand={}({})".format(type(self.operation).__name__, type(self.operand).__name__, self.operand)
    return output