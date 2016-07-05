# command
# author: Christophe VG <contact@christophe.vg>

# class implementation of ALP commands

# a D7A ALP Command consists of 1 or more ALP Actions
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.file import Offset, DataRequest, Data
from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.alp.operations.forward import Forward
from d7a.alp.operations.requests import ReadFileData
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operations.write_operations import WriteFileData
from d7a.alp.status_action import StatusAction, StatusActionOperandExtensions
from d7a.parse_error import ParseError
from d7a.sp.configuration import Configuration

from d7a.support.schema           import Validatable, Types
from d7a.alp.regular_action import RegularAction


class Command(Validatable):
  
  SCHEMA = [{
    "actions": Types.LIST(RegularAction),
    "interface_status": Types.OBJECT(StatusAction, nullable=True), # can be null for example when parsing DLL frames
    "flush_result": Types.OBJECT(StatusAction, nullable=True)
  }]

  def __init__(self, actions=[]):
    self.interface_status = None
    self.flush_result = None
    self.actions = []

    for action in actions:
      if type(action) == StatusAction:
        if action.status_operand_extension == StatusActionOperandExtensions.INTERFACE_STATUS:
          if self.interface_status != None:
            raise ParseError("An ALP command can contain one and only one Interface Status action")
          self.interface_status = action

        # TODO to be discussed in PAG
        if action.status_operand_extension == StatusActionOperandExtensions.FLUSH_RESULT_STATUS:
          if self.flush_result != None:
            raise ParseError("An ALP command can contain one and only one Flush Result Status action")

          self.flush_result = action

      if type(action) == RegularAction:
        self.actions.append(action)

    super(Command, self).__init__()

  def add_action(self, action):
    self.actions.append(action)

  def add_forward_action(self, interface_type=InterfaceType.HOST, interface_configuration=None):
    if interface_configuration is not None and interface_type == InterfaceType.HOST:
      raise ValueError("interface_configuration is not supported for interface_type HOST")

    if interface_type == InterfaceType.D7ASP:
      if interface_configuration is None:
        interface_configuration = Configuration()

      self.actions.append(
        RegularAction(
          operation=Forward(
            operand=InterfaceConfiguration(
              interface_id=InterfaceType.D7ASP,
              interface_configuration=interface_configuration
            )
          )
        )
      )

  @staticmethod
  def create_with_read_file_action(file_id, length, offset=0, interface_type=InterfaceType.HOST, interface_configuration=None):
    # default to host interface, when D7ASP interface is used prepend with Forward action
    cmd = Command()
    cmd.add_forward_action(interface_type, interface_configuration)
    cmd.add_action(
      RegularAction(
        operation=ReadFileData(
          operand=DataRequest(
            offset=Offset(id=file_id, offset=offset), # TODO offset size
            length=length
          )
        )
      )
    )

    return cmd

  @staticmethod
  def create_with_write_file_action(file_id, data, offset=0, interface_type=InterfaceType.HOST, interface_configuration=None):
    # default to host interface, when D7ASP interface is used prepend with Forward action
    cmd = Command()
    cmd.add_forward_action(interface_type, interface_configuration)
    cmd.add_action(
      RegularAction(
        operation=WriteFileData(
          operand=Data(
            offset=Offset(id=file_id, offset=offset), # TODO offset size
            data=data
          )
        )
      )
    )

    return cmd

  @staticmethod
  def create_with_return_file_data_action(file_id, data, interface_type=InterfaceType.HOST, interface_configuration=None):
    # default to host interface, when D7ASP interface is used prepend with Forward action
    cmd = Command()
    cmd.add_forward_action(interface_type, interface_configuration)
    cmd.add_action(
      RegularAction(
        operation=ReturnFileData(
          operand=Data(
            data=data,
            offset=Offset(id=file_id)
          )
        )
      )
    )

    return cmd

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