# command
# author: Christophe VG <contact@christophe.vg>

# class implementation of ALP commands

# a D7A ALP Command consists of 1 or more ALP Actions
from d7a.alp.operands.interface_status import InterfaceStatusOperand
from d7a.alp.status_action import StatusAction, StatusActionOperandExtensions
from d7a.parse_error import ParseError

from d7a.support.schema           import Validatable, Types
from d7a.alp.regular_action import RegularAction


class Command(Validatable):
  
  SCHEMA = [{
    "actions": Types.LIST(RegularAction),
    "interface_status": Types.OBJECT(StatusAction, nullable=True) # can be null for example when parsing DLL frames
  }]

  def __init__(self, actions=[]):
    self.interface_status = None
    self.actions = []

    for action in actions:
      if type(action) == StatusAction and action.status_operand_extension == StatusActionOperandExtensions.INTERFACE_STATUS:
        if self.interface_status != None: raise ParseError("An ALP command can contain one and only one Interface Status action")
        self.interface_status = action
      if type(action) == RegularAction:
        self.actions.append(action)

    super(Command, self).__init__()

  def __iter__(self):
    if self.interface_status is not None:
      for byte in self.interface_status:
        yield byte

    for action in self.actions:
      for byte in action:
        yield byte
