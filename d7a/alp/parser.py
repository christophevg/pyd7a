# parser
# author: Christophe VG <contact@christophe.vg>

# a parser for ALP commands

from bitstring                    import ConstBitStream, ReadError

from d7a.types.ct                 import CT
from d7a.sp.status                import Status
from d7a.tp.addressee             import Addressee
from d7a.alp.command              import Command
from d7a.alp.payload              import Payload
from d7a.alp.action               import Action
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operations.requests  import RequestFileData
from d7a.alp.operands.file        import Offset, Data, DataRequest

class ParseError(Exception): pass

class Parser(object):

  def __init__(self):
    self.buffer = []

  def shift_buffer(self, start):
    self.buffer = self.buffer[start:]
    return self

  def parse(self, msg):
    self.buffer.extend(msg)
    return self.parse_buffer()
    
  def parse_buffer(self):
    parsed = 0
    cmds   = []

    while True:
      (cmd, info) = self.parse_one_command_from_buffer()
      if cmd is None: break
      parsed += info["parsed"]
      cmds.append(cmd)
      
    info["parsed"] = parsed
    return (cmds, info)

  def parse_one_command_from_buffer(self):
    retry       = True    # until we have one or don't have enough
    errors      = []
    cmd         = None
    bits_parsed = 0
    while retry and len(self.buffer) > 0:
      try:
        s           = ConstBitStream(bytes=self.buffer)
        cmd         = self.parse_alp_command(s)
        bits_parsed = s.pos
        self.shift_buffer(bits_parsed/8)
        retry = False         # got one, carry on
      except ReadError:       # not enough to read, carry on and wait for more
        retry = False
      except ParseError as e: # actual problem with current buffer, need to skip
        errors.append({
          "error"   : e.args[0],
          "buffer"  : list(self.buffer),
          "pos"     : s.pos,
          "skipped" : self.skip_bad_buffer_content()
        })
      
    info = {
      "parsed" : bits_parsed,
      "buffer" : len(self.buffer) * 8,
      "errors" : errors
    }
    return (cmd, info)    

  def skip_bad_buffer_content(self):
    # skip until we find 0xd7, which might be a valid starting point
    try:
      self.buffer.pop(0)                      # first might be 0xd7
      pos = self.buffer.index(0xd7)
      self.buffer = self.buffer[pos:]
      return pos + 1
    except IndexError:                        # empty buffer
      return 0
    except ValueError:                        # empty buffer, reported by .index
      skipped = len(self.buffer) + 1          # popped first item already
      self.buffer = []
      return skipped

  def parse_alp_command(self, s):
    interface = None
    group     = None
    resp      = None
    opcode    = None
    operation = None
    error     = None
    _         = self.parse_alp_interface_id(s)
    return Command(
      interface = self.parse_alp_interface_status(s),
      payload   = self.parse_alp_payload(s)
    )

  def parse_alp_interface_id(self, s):
    b = s.read("uint:8")
    if b != 0xd7: raise ParseError("expected 0x7d, found {0}".format(b))

  def parse_alp_interface_status(self, s):
    nls         = s.read("bool")
    missed      = s.read("bool")
    retry       = s.read("bool")
    _           = s.read("pad:2" )
    state       = s.read("uint:3")
    fifo_token  = s.read("uint:8")
    request_id  = s.read("uint:8")
    response_to = self.parse_ct(s)
    addressee   = self.parse_addressee(s)

    return Status(nls=nls, missed=missed, retry=retry, state=state,
                  fifo_token=fifo_token, request_id=request_id,
                  response_to=response_to, addressee=addressee)

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

  def parse_alp_payload(self, s):
    # TODO: extend to multiple actions, only one supported right now
    action = self.parse_alp_action(s)
    return Payload(actions=[action])

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
