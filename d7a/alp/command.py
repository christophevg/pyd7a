# command
# author: Christophe VG <contact@christophe.vg>

# class implementation of ALP commands

# a D7A ALP Command consists of 1 or more ALP Actions
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.file import Offset, DataRequest, Data
from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.alp.operations.forward import Forward
from d7a.alp.operations.requests import ReadFileData
from d7a.alp.operations.write_operations import WriteFileData
from d7a.alp.status_action import StatusAction, StatusActionOperandExtensions
from d7a.parse_error import ParseError
from d7a.sp.configuration import Configuration

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

  @staticmethod
  def create_with_read_file_action(file_id, length, offset=0, interface_type=InterfaceType.HOST):
    # default to host interface, when D7ASP interface is used prepend with Forward action
    actions = []
    if interface_type == InterfaceType.D7ASP:
      actions.append(
        RegularAction(
          operation=Forward(
            operand=InterfaceConfiguration(
              interface_id=InterfaceType.D7ASP,
              interface_configuration=Configuration(
                # TODO
              )
            )
          )
        )
      )

    actions.append(
      RegularAction(
        operation=ReadFileData(
          operand=DataRequest(
            offset=Offset(id=file_id, offset=offset), # TODO offset size
            length=length
          )
        )
      )
    )

    return Command(actions=actions)

  @staticmethod
  def create_with_write_file_action(file_id, data=[], offset=0, interface_type=InterfaceType.HOST):
    # default to host interface, when D7ASP interface is used prepend with Forward action
    actions = []
    if interface_type == InterfaceType.D7ASP:
      actions.append(
        RegularAction(
          operation=Forward(
            operand=InterfaceConfiguration(
              interface_id=InterfaceType.D7ASP,
              interface_configuration=Configuration(
                # TODO
              )
            )
          )
        )
      )

    actions.append(
      RegularAction(
        operation=WriteFileData(
          operand=Data(
            offset=Offset(id=file_id, offset=offset), # TODO offset size
            data=data
          )
        )
      )
    )

    return Command(actions=actions)

  def __iter__(self):
    if self.interface_status is not None:
      for byte in self.interface_status:
        yield byte

    for action in self.actions:
      for byte in action:
        yield byte

  def __str__(self):
    output = "Command actions:\n"
    for action in self.actions:
      output = output + "\taction: {}\n".format(action)

    if self.interface_status is not None:
      output = output + "interface status: {}\n".format(self.interface_status)
    return output