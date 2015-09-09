# qos
# author: Christophe VG <contact@christophe.vg>

# class implementation of qos parameters

# D7ASP QOS (Parameters)
#
# QOS_CTRL      1 byte:
#   b7-b5   RFU
#   b4      ACK_NOT_VOID  Respond only if the Acknowledge Return Template 
#                         bitmap is not empty.
#   b3-b2   RFU
#   b1-b0   RESP_MOD      Response Mode
# ACK_PERIOD    1 byte Maximum number of Requests transmitted between two D7ATP 
#                      ACK template requests.
# RETRY_SINGLE  1 byte Single retry limit. The maximum number of retries of a 
#                      Request with particular ID. 0 - no limit
# RETRY_TOTAL   1 byte Total retries limit. The maximum total number of
#                      retries. 0 - no limit

from d7a.support.schema import Validatable, Types
  
class QoS(Validatable):
  
  # [4.2.2] Data transmitted by a sensor may be considered received if it is 
  # acknowledged by at least one gateway (any-cast) or by all gateways 
  # (all-cast)
  NO_CAST  = 0
  ALL_CAST = 1
  ANY_CAST = 2

  SCHEMA = [{
    "ack_not_void" : Types.BOOLEAN(),
    "resp_mod"     : Types.ENUM([ None, NO_CAST, ALL_CAST, ANY_CAST ]),
    "ack_period"   : Types.BYTE(),
    "retry_single" : Types.BYTE(),
    "retry_total"  : Types.BYTE()
  }]
  
  def __init__(self, ack_not_void=False, resp_mod=None, ack_period=0,
                     retry_single=0, retry_total=0):
    self.ack_not_void = ack_not_void
    self.resp_mod     = 0 if resp_mod is None else resp_mod
    self.ack_period   = ack_period
    self.retry_single = retry_single
    self.retry_total  = retry_total
    super(QoS, self).__init__()
