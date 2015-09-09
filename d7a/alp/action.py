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

from d7a.support.schema     import Validatable, Types

from d7a.alp.operations.nop import NoOperation

class Action(Validatable):

  SCHEMA = [{
    "group"    : Types.BOOLEAN(),
    "resp"     : Types.BOOLEAN(),
    "op"       : Types.BITS(6),
    "operation": Types.OBJECT(),
    "operand"  : Types.OBJECT(nullable=True)
  }]

  def __init__(self, group=False, resp=False,
               operation=NoOperation(), operand=None):
    self.group     = group
    self.resp      = resp
    self.operation = operation
    self.operand   = operand
    super(Action, self).__init__()

  @property
  def op(self):
    return self.operation.op
