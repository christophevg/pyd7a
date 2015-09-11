# parser
# author: Christophe VG <contact@christophe.vg>

# a parser for ALP commands

# a received ALP command consists of
# - ALP Status
# - ALP Payload

from bitstring                    import ConstBitStream, ReadError

from d7a.types.ct                 import CT
from d7a.sp.status                import Status
from d7a.tp.addressee             import Addressee
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operands.file        import Offset, Data

class Parser(object):

  def parse(self, msg):
    self.s = ConstBitStream(bytes=msg)
    return self.parse_alp_command()

  def parse_alp_command(self):
    interface = None
    group     = None
    resp      = None
    opcode    = None
    operation = None
    error     = None
    try:
      _         = self.parse_alp_interface_id()
      interface = self.parse_alp_interface_status()
      (group, resp, opcode, operation) = self.parse_alp_action()
    except ReadError:   # read past end of stream
      error = "read past end of stream"
    return {
      "interface" : None if interface is None else interface.as_dict(),
      "group"     : group,
      "resp"      : resp,
      "opcode"    : opcode,
      "operation" : None if operation is None else operation.as_dict(),
      "_stream"    : {
        "pos" : self.s.pos,
        "len" : len(self.s)
      },
      "_error"     : error
    }

  def parse_alp_interface_id(self):
    b = self.s.read("uint:8")
    if b != 0xd7: raise Exception("expected 0xd7, found {0}".format(b))

  def parse_alp_interface_status(self):
    nls         = self.s.read("bool")
    missed      = self.s.read("bool")
    retry       = self.s.read("bool")
    _           = self.s.read("pad:2" )
    state       = self.s.read("uint:3")
    fifo_token  = self.s.read("uint:8")
    request_id  = self.s.read("uint:8")
    response_to = self.parse_ct()
    addressee   = self.parse_addressee()

    return Status(nls=nls, missed=missed, retry=retry, state=state,
                  fifo_token=fifo_token, request_id=request_id,
                  response_to=response_to, addressee=addressee)

  def parse_ct(self):
    exp  = self.s.read("uint:3")
    mant = self.s.read("uint:5")
    return CT(exp=exp, mant=mant)

  def parse_addressee(self):
    _     = self.s.read("pad:2")
    ucast = self.s.read("bool")
    vid   = self.s.read("bool")
    cl    = self.s.read("uint:4")
    l     = Addressee.length_for(ucast=ucast,vid=vid)
    id    = self.s.read("uint:"+str(l*8)) if l > 0 else None
    return Addressee(ucast=ucast, vid=vid, cl=cl, id=id)

  def parse_alp_action(self):
    group     = self.s.read("bool")
    resp      = self.s.read("bool")
    op        = self.s.read("uint:6")
    try:
      operation = {
        32 : self.parse_slp_return_file_data_operation
      }[op]()
    except KeyError:
      raise NotImplementedError("alp_action " + str(op) + " is not implemented")
    return (group, resp, op, operation)

  def parse_slp_return_file_data_operation(self):
    operand = self.parse_alp_return_file_data_operand()
    return ReturnFileData(operand=operand)
    

  def parse_alp_return_file_data_operand(self):
    offset = self.parse_offset()
    length = self.s.read("uint:8")
    data   = self.s.read("bytes:" + str(length))
    return Data(offset=offset, data=map(ord,data))

  def parse_offset(self):
    id     = self.s.read("uint:8")
    size   = self.s.read("uint:2") # + 1 = already read
    
    offset = self.s.read("uint:" + str(6+(size * 8)))
    return Offset(id=id, size=size+1, offset=offset)
