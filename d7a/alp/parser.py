# parser
# author: Christophe VG <contact@christophe.vg>

# a parser for ALP commands
import struct

from d7a.alp.command              import Command
from d7a.alp.action               import Action
from d7a.alp.operands.interface_status import InterfaceStatusOperand
from d7a.alp.operations.interface_status import InterfaceStatus
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operations.requests  import RequestFileData
from d7a.alp.operands.file        import Offset, Data, DataRequest
from d7a.parse_error              import ParseError
from d7a.sp.status import Status
from d7a.tp.addressee import Addressee
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

    return Command(actions = actions)

  def parse_alp_action(self, s):
    # TODO meaning of first 2 bits depend on action type
    group     = s.read("bool")
    resp      = s.read("bool")
    op        = s.read("uint:6")
    try:
      operation = {
        1 :   self.parse_alp_read_file_data_operation,
        32 :  self.parse_alp_return_file_data_operation,
        51 :  self.parse_alp_interface_status_operation
      }[op](s)
    except KeyError:
      raise ParseError("alp_action " + str(op) + " is not implemented")
    return Action(group=group, resp=resp, operation=operation)

  def parse_alp_read_file_data_operation(self, s):
    operand = self.parse_alp_file_data_request_operand(s)
    return RequestFileData(operand=operand)

  def parse_alp_file_data_request_operand(self, s):
    offset = self.parse_offset(s)
    length = s.read("uint:8")
    return DataRequest(length=length, offset=offset)

  def parse_alp_return_file_data_operation(self, s):
    operand = self.parse_alp_return_file_data_operand(s)
    return ReturnFileData(operand=operand)

  def parse_alp_return_file_data_operand(self, s):
    offset = self.parse_offset(s)
    length = s.read("uint:8")
    data   = s.read("bytes:" + str(length))
    return Data(offset=offset, data=map(ord,data))

  def parse_alp_interface_status_operation(self, s):
    interface_id = s.read("uint:8")
    try:
      interface_status_operation = {
        0x00 :  self.parse_alp_interface_status_host,
        0xd7 :  self.parse_alp_interface_status_d7asp,
      }[interface_id](s)
      return interface_status_operation
    except KeyError:
      raise ParseError("Received ALP Interface status for interface " + str(interface_id) + " which is not implemented")

  def parse_alp_interface_status_host(self, s):
    pass # no interface status defined for host interface

  def parse_alp_interface_status_d7asp(self, s):
    channel_id  = map(ord, s.read("bytes:3")) # TODO parse
    rssi        = struct.unpack("<h", s.read("bytes:2"))[0]
    link_budget = s.read("uint:8")  # TODO parse
    nls         = s.read("bool")
    missed      = s.read("bool")
    retry       = s.read("bool")
    _           = s.read("pad:2" )
    state       = s.read("uint:3")
    fifo_token  = s.read("uint:8")
    request_id  = s.read("uint:8")
    response_to = self.parse_ct(s)
    addressee   = self.parse_addressee(s)

    status = Status(channel_id=channel_id, rssi= rssi, link_budget=link_budget,
                  nls=nls, missed=missed, retry=retry, state=state,
                  fifo_token=fifo_token, request_id=request_id,
                  response_to=response_to, addressee=addressee)

    return InterfaceStatus(operand=InterfaceStatusOperand(interface_id=0xd7, interface_status=status))


  def parse_offset(self, s):
    id     = s.read("uint:8")
    size   = s.read("uint:2") # + 1 = already read

    offset = s.read("uint:" + str(6+(size * 8)))
    return Offset(id=id, size=size+1, offset=offset)

  def parse_ct(self, s):
    exp  = s.read("uint:3")
    mant = s.read("uint:5")
    return CT(exp=exp, mant=mant)

  def parse_addressee(self, s):
    _     = s.read("pad:2")
    hasid = s.read("bool")
    vid   = s.read("bool")
    cl    = s.read("uint:4")
    l     = Addressee.length_for(hasid=hasid, vid=vid)
    id    = s.read("uint:"+str(l*8)) if l > 0 else None
    return Addressee(vid=vid, cl=cl, id=id)