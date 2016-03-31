# parser
# author: Christophe VG <contact@christophe.vg>

# a parser for ALP commands

from d7a.alp.command              import Command
from d7a.alp.action               import Action
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operations.requests  import RequestFileData
from d7a.alp.operands.file        import Offset, Data, DataRequest
from d7a.parse_error              import ParseError

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

  # def parse_alp_interface_status(self, s):
  #   nls         = s.read("bool")
  #   missed      = s.read("bool")
  #   retry       = s.read("bool")
  #   _           = s.read("pad:2" )
  #   state       = s.read("uint:3")
  #   fifo_token  = s.read("uint:8")
  #   request_id  = s.read("uint:8")
  #   response_to = self.parse_ct(s)
  #   addressee   = self.parse_addressee(s)
  #
  #   return Status(nls=nls, missed=missed, retry=retry, state=state,
  #                 fifo_token=fifo_token, request_id=request_id,
  #                 response_to=response_to, addressee=addressee)

  def parse_alp_action(self, s):
    group     = s.read("bool")
    resp      = s.read("bool")
    op        = s.read("uint:6")
    try:
      operation = {
        1 :   self.parse_alp_read_file_data_operation,
        32 :  self.parse_alp_return_file_data_operation
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

  def parse_offset(self, s):
    id     = s.read("uint:8")
    size   = s.read("uint:2") # + 1 = already read

    offset = s.read("uint:" + str(6+(size * 8)))
    return Offset(id=id, size=size+1, offset=offset)
