# (FIFO) configuration
# author: Christophe VG <contact@christophe.vg>

# class implementation of (FIFO) configuration

from d7a.support.schema   import Validatable, Types

from d7a.types.ct         import CT

from d7a.sp.qos           import QoS
from d7a.sp.session       import States

from d7a.d7anp.addressee import Addressee

class Configuration(Validatable):

  SCHEMA = [{
    "qos"        : Types.OBJECT(QoS),
    "dorm_to"    : Types.OBJECT(CT),
    "addressee"  : Types.OBJECT(Addressee)
  }]

  def __init__(self, qos=QoS(), dorm_to=CT(), addressee=Addressee()):
    self.qos         = qos
    self.dorm_to     = dorm_to
    self.addressee   = addressee
    super(Configuration, self).__init__()

  def __iter__(self):
    for byte in self.qos: yield byte
    for byte in self.dorm_to: yield byte
    for byte in self.addressee: yield byte

  def __str__(self):
    return str(self.as_dict())