# qos
# author: Christophe VG <contact@christophe.vg>

# class implementation of qos parameters

from d7a.support.schema import Validatable, Types
  
class QoS(Validatable):

  RESP_MODE_NO = 0
  RESP_MODE_ALL = 1
  RESP_MODE_ANY = 2
  RESP_MODE_NO_RPT = 4
  RESP_MODE_ON_ERROR = 5
  RESP_MODE_PREFERRED = 6

  SCHEMA = [{
    "nls": Types.BOOLEAN(),
    "stop_on_err": Types.BOOLEAN(),
    "record" : Types.BOOLEAN(),
    "resp_mod"     : Types.ENUM([ None, RESP_MODE_NO, RESP_MODE_ALL, RESP_MODE_ANY, RESP_MODE_NO_RPT,
                                  RESP_MODE_ON_ERROR, RESP_MODE_ON_ERROR]),
  }]
  
  def __init__(self, nls=False, resp_mod=RESP_MODE_NO, stop_on_err=False, record=False):
    self.nls          = nls
    self.resp_mod     = resp_mod
    self.stop_on_err  = stop_on_err
    self.record       = record
    super(QoS, self).__init__()

  def __iter__(self):
    byte = 0
    if self.nls: byte |= 1 << 7
    if self.stop_on_err: byte |= 1 << 6
    if self.record: byte |= 1 << 5
    # rfu
    byte += self.resp_mod
    yield byte
