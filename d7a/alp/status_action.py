from d7a.alp.action import Action
from d7a.alp.operations.nop import NoOperation
from d7a.alp.operations.operation import Operation
from d7a.support.schema import Types

__author__ = 'glenn'

class StatusActionOperandExtensions(object):
  ACTION_STATUS = 0
  INTERFACE_STATUS = 1
  ALL   = [ ACTION_STATUS, INTERFACE_STATUS ]

  @staticmethod
  def SCHEMA():
    return { "type": "integer", "allowed" : StatusActionOperandExtensions.ALL }


class StatusAction(Action):
  SCHEMA = [{
    "status_operand_extension"    : Types.INTEGER(values=StatusActionOperandExtensions.ALL),
    "operation": Types.OBJECT(Operation),
    "operand"  : Types.OBJECT(nullable=True)  # there is no Operand base-class
  }]

  def __init__(self, status_operand_extension, operation, operand):
    self.status_operand_extension = status_operand_extension
    self.operand = operand
    self.operation = operation
    super(StatusAction, self).__init__()

  def __iter__(self):
    byte = 0
    if self.resp:  byte |= self.status_operand_extension << 6
    byte += self.op
    yield byte

    for byte in self.operation: yield byte