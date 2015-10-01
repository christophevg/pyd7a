# Status (aka Reception)
# author: Christophe VG <contact@christophe.vg>

# class implementation of status meta-data

# D7ASP Status
#
# STATUS      1 byte      Slave D7ASP Status 9.2.9.1
#   b7    NLS     NWL Security Enabled
#   b6    MISSED  Always 0 for Responses. For Requests - set to 0 when the 
#                 D7ATP ACK_BITMAP is empty.
#   b5    RETRY   Always 0 for Responses. For Request - depends on the value of 
#                 the D7ATP Transaction ID bit in ACK_BITMAP before reception 
#                 of the current Request. When set to 1, a segment with the 
#                 same REQUEST_ID and FIFO_TOKEN has already been vectored to 
#                 upper layer.
#   b4-b3 RFU
#   b2-b0 STATE   Session State
# FIFO_TOKEN  1 byte      Value of the D7ATP Dialog ID
# REQUEST_ID  1 bytes     Value of the D7ATP Transaction ID
# RESPONSE_TO 1 byte      D7ATP Addressee Access Profile's Tc in Compressed 
#                         Time Format.
# ADDRESSEE   1/3/9 bytes D7ATP Addressee

from d7a.support.schema   import Validatable, Types

from d7a.types.ct         import CT

from d7a.tp.addressee     import Addressee

from d7a.sp.session       import States

class Status(Validatable):

  SCHEMA = [{
    "nls"        : Types.BOOLEAN(),
    "missed"     : Types.BOOLEAN(),
    "retry"      : Types.BOOLEAN(),
    "state"      : States.SCHEMA(),
    "fifo_token" : Types.BYTE(),
    "request_id" : Types.BYTE(),
    "response_to": Types.OBJECT(CT),
    "addressee"  : Types.OBJECT(Addressee)
  }]

  def __init__(self, nls=False, missed=False, retry=False, state=States.IDLE,
                     fifo_token=0, request_id=0, response_to=CT(),
                     addressee=Addressee()):
    self.nls         = nls
    self.missed      = missed
    self.retry       = retry
    self.state       = state
    self.fifo_token  = fifo_token
    self.request_id  = request_id
    self.response_to = response_to
    self.addressee   = addressee
    super(Status, self).__init__()

  def __iter__(self):
    byte = 0;
    if self.nls:    byte |= 1 << 7
    if self.missed: byte |= 1 << 6
    if self.retry:  byte |= 1 << 5
    # padding << 4 & << 3
    if self.state:  byte += self.state  # 2 1 0
    yield byte

    yield chr(self.fifo_token)
    yield chr(self.request_id)

    for byte in self.response_to: yield byte
    for byte in self.addressee: yield byte
