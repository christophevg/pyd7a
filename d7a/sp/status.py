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
import struct

from d7a.support.schema   import Validatable, Types
from d7a.types.ct         import CT
from d7a.d7anp.addressee import Addressee

class Status(Validatable):

  SCHEMA = [{
    "channel_header"    : Types.BYTE(), # TODO parse
    "channel_index" : Types.INTEGER(),
    "rx_level"      : Types.BYTE(),
    "link_budget": Types.BYTE(),
    "target_rx_level": Types.BYTE(),
    "nls"        : Types.BOOLEAN(),
    "missed"     : Types.BOOLEAN(),
    "retry"      : Types.BOOLEAN(),
    "ucast"      : Types.BOOLEAN(),
    "fifo_token" : Types.BYTE(),
    "seq_nr"     : Types.BYTE(),
    "response_to": Types.OBJECT(CT),
    "addressee"  : Types.OBJECT(Addressee)
  }]

  def __init__(self, channel_header, channel_index, rx_level, link_budget, target_rx_level, nls, missed, retry, unicast,
                     fifo_token, seq_nr, response_to, addressee):
    self.channel_header  = channel_header
    self.channel_index  = channel_index
    self.rx_level    = rx_level
    self.link_budget = link_budget
    self.target_rx_level = target_rx_level
    self.nls         = nls
    self.missed      = missed
    self.retry       = retry
    self.unicast       = unicast
    self.fifo_token  = fifo_token
    self.seq_nr  = seq_nr
    self.response_to = response_to
    self.addressee   = addressee
    super(Status, self).__init__()

  def __iter__(self):
    yield self.channel_header
    for byte in bytearray(struct.pack("<h", self.channel_index)): yield byte
    yield self.rx_level
    yield self.link_budget
    yield self.target_rx_level
    byte = 0
    if self.nls:    byte |= 1 << 7
    if self.missed: byte |= 1 << 6
    if self.retry:  byte |= 1 << 5
    if self.unicast:  byte |= 1 << 4
    yield byte
    yield chr(self.fifo_token)
    yield chr(self.seq_nr)
    for byte in self.response_to: yield byte
    for byte in self.addressee: yield byte

  def __str__(self):
    return "unicast={}, nls={}, retry={}, missed={}, fifo_token={}, rx_level={}, " \
          "seq_nr={}, target_rx_level={}, addressee={}, response_to={}, link_budget={}, channel_header={}".format(
      self.unicast,
      self.nls,
      self.retry,
      self.missed,
      self.fifo_token,
      self.rx_level,
      self.seq_nr,
      self.target_rx_level,
      self.addressee,
      self.response_to,
      self.link_budget,
      self.channel_header
    )