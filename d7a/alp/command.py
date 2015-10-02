# command
# author: Christophe VG <contact@christophe.vg>

# class implementation of ALP commands

# a D7A ALP Command consists of
# - ALP Interface Configuration/Status
# - ALP Payload

from d7a.support.schema           import Validatable, Types

from d7a.sp.status                import Status
from d7a.sp.configuration         import Configuration
from d7a.alp.payload              import Payload

class Command(Validatable):
  
  SCHEMA = [{
    "interface": Types.OBJECT(Status),
    "payload"  : Types.OBJECT(Payload)
  },
  {
    "interface": Types.OBJECT(Configuration),
    "payload"  : Types.OBJECT(Payload)
  }]

  def __init__(self, interface=None, payload=None):
    self.interface = interface
    self.payload   = payload
    super(Command, self).__init__()

  def __iter__(self):
    yield chr(0xd7)
    for byte in self.interface: yield byte
    for byte in self.payload:   yield byte
