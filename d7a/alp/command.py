# command
# author: Christophe VG <contact@christophe.vg>

# class implementation of ALP commands

# a D7A ALP Command consists of 1 or more ALP Actions
from d7a.alp.operations.interface_status import InterfaceStatus
from d7a.parse_error import ParseError

from d7a.support.schema           import Validatable, Types
from d7a.alp.action              import Action

class Command(Validatable):
  
  SCHEMA = [{
    "actions": Types.LIST(Action),
    "interface_status": Types.OBJECT(InterfaceStatus, nullable=True) # can be null for example when parsing DLL frames
  }]


  def __init__(self, actions=[]):
    self.actions = actions
    self.interface_status = None
    for action in self.actions:
      if type(action.operation) == InterfaceStatus:
        if self.interface_status != None: raise ParseError("An ALP command can contain one and only one Interface Status action")
        self.interface_status = action.operation

    super(Command, self).__init__()

  def __iter__(self):
    for action in self.actions:
      for byte in action:
        yield byte
