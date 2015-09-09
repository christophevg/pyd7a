# (FIFO) configuration
# author: Christophe VG <contact@christophe.vg>

# class implementation of (FIFO) configuration

# D7ASP (FIFO) Configuration
#
# FIFO_CTRL 1 byte:
#   b7    NLS           Enable NWL Security
#   b6    RFU
#   b5    STOP_ON_ERR   Terminate if PROGRESS_BITMAP is not equal to 
#                       SUCCESS_BITMAP (9.2.8)
#   b4    PREFERRED     Manage dynamically the FIFO Addressee when QoS mode is 
#                       set to any-cast.(9.2.3)
#   b3    RFU
#   b2-b0 STATE         Session State
# QoS       4 bytes     Quality of Service
# DORM_TO   1 byte      Dormant Timeout in Compressed Time Format.
# START_ID  1 byte      Start Request identifier
# ADDRESSEE 1/3/9 bytes D7ATP Addressee

from d7a.support.schema   import Validatable, Types

from d7a.types.ct         import CT

from d7a.sp.qos           import QoS
from d7a.sp.session       import States

from d7a.tp.addressee     import Addressee

class Configuration(Validatable):

  SCHEMA = [{
    "nls"        : Types.BOOLEAN(),
    "stop_on_err": Types.BOOLEAN(),
    "preferred"  : Types.BOOLEAN(),
    "state"      : States.SCHEMA(),
    "qos"        : Types.OBJECT(),
    "dorm_to"    : Types.OBJECT(),
    "start_id"   : Types.BYTE(),
    "addressee"  : Types.OBJECT()
  }]

  def __init__(self, nls=False, stop_on_err=False, preferred=False,
                     state=States.IDLE, qos=QoS(), dorm_to=CT(), start_id=0,
                     addressee=Addressee()):
    self.nls         = nls
    self.stop_on_err = stop_on_err
    self.preferred   = preferred
    self.state       = state
    self.qos         = qos
    self.dorm_to     = dorm_to
    self.start_id    = start_id
    self.addressee   = addressee
    super(Configuration, self).__init__()
