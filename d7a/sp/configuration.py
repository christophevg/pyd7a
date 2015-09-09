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

from d7a.support.schema   import Validatable

from d7a.types.ct         import CT

from d7a.sp.qos           import QoS
from d7a.tp.addressee     import Addressee

class Configuration(Validatable):

  # SESSION STATES
  IDLE    = 0  # Inactive Session
  DORMANT = 1  # The group of Requests needs to be executed within a timeout 
               # period, which has not expired. After completion of the period, 
               # the Dormant Session is transformed into Pending Session.
  PENDING = 2  # The group of Requests needs to be executed as soon as possible.
  ACTIVE  = 3  # The Session is being currently executed using the D7A Session 
               # Protocol.
  DONE    = 4  # Terminated Session

  SCHEMA = [{
    "nls"        : { "type": "boolean", "nullable": False },
    "stop_on_err": { "type": "boolean", "nullable": False },
    "preferred"  : { "type": "boolean", "nullable": False },
    "state"      : { "type": "integer", "allowed" : [ IDLE, DORMANT, PENDING, ACTIVE, DONE ]},
    "qos"        : { "nullable": False },
    "dorm_to"    : { "nullable": False },
    "start_id"   : { "type": "integer", "nullable": False, "min": 0, "max": 0xFF },
    "addressee"  : { "nullable": False }
  }]

  def __init__(self, nls=False, stop_on_err=False, preferred=False, state=IDLE,
                     qos=QoS(), dorm_to=CT(), start_id=0, addressee=Addressee()):
    self.nls         = nls
    self.stop_on_err = stop_on_err
    self.preferred   = preferred
    self.state       = state
    self.qos         = qos
    self.dorm_to     = dorm_to
    self.start_id    = start_id
    self.addressee   = addressee
    super(Configuration, self).__init__()
