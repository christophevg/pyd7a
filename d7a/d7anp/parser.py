
from bitstring import ConstBitStream, ReadError
from d7a.d7anp.frame import Frame
from d7a.d7anp.control import Control


class Parser(object):

  def parse(self, bitstream, payload_length):
    control = Control(
      has_network_layer_security=bitstream.read("bool"),
      has_multi_hop=bitstream.read("bool"),
      has_origin_access_id=bitstream.read("bool"),
      is_origin_access_id_vid=bitstream.read("bool"),
      origin_access_class=bitstream.read("uint:4")
    )
    payload_length = payload_length - 1 # substract control

    assert control.has_multi_hop == False, "Not implemented yet"
    assert control.has_network_layer_security == False, "Not implemented yet"

    if control.has_origin_access_id:
      if control.is_origin_access_id_vid:
        origin_access_id = map(ord, bitstream.read("bytes:2"))
        payload_length = payload_length - 2
      else:
        origin_access_id = map(ord, bitstream.read("bytes:8"))
        payload_length = payload_length - 8
    else:
      origin_access_id = []

    payload=map(ord,bitstream.read("bytes:" + str(payload_length)))
    return Frame(control=control, origin_access_id=origin_access_id, payload=payload)
