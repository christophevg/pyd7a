# parser
# author: Christophe VG <contact@christophe.vg>

# a parser for ALP commands
import struct

from d7a.alp.command              import Command
from d7a.alp.operands.interface_status import InterfaceStatusOperand
from d7a.alp.operations.status import InterfaceStatus
from d7a.alp.status_action import StatusAction, StatusActionOperandExtensions
from d7a.alp.regular_action import RegularAction
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operations.requests  import ReadFileData
from d7a.alp.operands.file        import Offset, Data, DataRequest
from d7a.parse_error              import ParseError
from d7a.sp.status import Status
from d7a.d7anp.addressee import Addressee
from d7a.types.ct import CT


class Parser(object):

  def parse(self, s, cmd_length):
    actions = []
    if cmd_length != 0:
      startpos = s.bytepos
      alp_bytes_parsed = 0
      while alp_bytes_parsed < cmd_length:
        action = self.parse_alp_action(s)
        actions.append(action)
        alp_bytes_parsed = alp_bytes_parsed + (s.bytepos - startpos)

    cmd = Command(actions = actions)
    return cmd

  def parse_alp_action(self, s):
    # meaning of first 2 bits depend on action opcode
    b7     = s.read("bool")
    b6      = s.read("bool")
    op        = s.read("uint:6")
    try:
      return{
        1 :   self.parse_alp_read_file_data_action,
        32 :  self.parse_alp_return_file_data_action,
        34 :  self.parse_alp_return_status_action
      }[op](b7, b6, s)
    except KeyError:
      raise ParseError("alp_action " + str(op) + " is not implemented")

  def parse_alp_read_file_data_action(self, b7, b6, s):
    operand = self.parse_alp_file_data_request_operand(s)
    return RegularAction(group=b7,
                  resp=b6,
                  operation=ReadFileData(operand=operand))

  def parse_alp_file_data_request_operand(self, s):
    offset = self.parse_offset(s)
    length = s.read("uint:8")
    return DataRequest(length=length, offset=offset)

  def parse_alp_return_file_data_action(self, b7, b6, s):
    operand = self.parse_alp_return_file_data_operand(s)
    return RegularAction(group=b7,
                        resp=b6,
                        operation=ReturnFileData(operand=operand))

  def parse_alp_return_file_data_operand(self, s):
    offset = self.parse_offset(s)
    length = s.read("uint:8")
    data   = s.read("bytes:" + str(length))
    return Data(offset=offset, data=map(ord,data))

  def parse_alp_return_status_action(self, b7, b6, s):
    if b7:
      raise ParseError("Status Operand extension 2 and 3 is RFU")

    if b6: # interface status
      interface_id = s.read("uint:8")
      try:
        interface_status_operation = {
          0x00 :  self.parse_alp_interface_status_host,
          0xd7 :  self.parse_alp_interface_status_d7asp,
        }[interface_id](s)
        return StatusAction(operation=interface_status_operation,
                            status_operand_extension=StatusActionOperandExtensions.INTERFACE_STATUS)
      except KeyError:
        raise ParseError("Received ALP Interface status for interface " + str(interface_id) + " which is not implemented")
    else: # action status
      pass # TODO


  def parse_alp_interface_status_host(self, s):
    pass # no interface status defined for host interface

  def parse_alp_interface_status_d7asp(self, s):
    channel_header = s.read("uint:8") # TODO parse
    channel_index = struct.unpack("<h", s.read("bytes:2"))[0]
    rx_level = s.read("int:8")
    link_budget = s.read("uint:8")
    target_rx_level = s.read("uint:8")
    nls         = s.read("bool")
    missed      = s.read("bool")
    retry       = s.read("bool")
    unicast     = s.read("bool" )
    _           = s.read("pad:4")
    fifo_token  = s.read("uint:8")
    seq_nr  = s.read("uint:8")
    response_to = CT.parse(s)
    addressee   = Addressee.parse(s)

    status = Status(channel_header=channel_header, channel_index=channel_index, rx_level=rx_level, link_budget=link_budget,
                  target_rx_level=target_rx_level, nls=nls, missed=missed, retry=retry, unicast=unicast,
                  fifo_token=fifo_token, seq_nr=seq_nr,
                  response_to=response_to, addressee=addressee)

    return InterfaceStatus(operand=InterfaceStatusOperand(interface_id=0xd7, interface_status=status))


  def parse_offset(self, s):
    id     = s.read("uint:8")
    size   = s.read("uint:2") # + 1 = already read

    offset = s.read("uint:" + str(6+(size * 8)))
    return Offset(id=id, size=size+1, offset=offset)
