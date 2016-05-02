
from bitstring import ConstBitStream, ReadError
from d7a.d7atp.frame import Frame
from d7a.d7atp.control import Control
from d7a.alp.parser import Parser as AlpParser

class Parser(object):

  def parse(self, bitstream, payload_length):
    is_dialog_start = bitstream.read("bool")
    is_dialog_end = bitstream.read("bool")
    _ = bitstream.read("pad:2"),
    is_ack_return_template_requested = bitstream.read("bool")
    is_ack_not_void = bitstream.read("bool")
    is_ack_recorded = bitstream.read("bool")
    _ = bitstream.read("pad:1")
    payload_length = payload_length - 1 # subtract control byte

    control = Control(is_dialog_start, is_dialog_end, is_ack_return_template_requested,
                      is_ack_not_void, is_ack_recorded)

    dialog_id = bitstream.read("uint:8")
    payload_length = payload_length - 1

    transaction_id = bitstream.read("uint:8")
    payload_length = payload_length - 1

    ack_template = None
    if is_ack_not_void:
      transaction_id_start = bitstream.read("uint:8")
      payload_length = payload_length - 1
      transaction_id_stop = bitstream.read("uint:8")
      payload_length = payload_length - 1
      assert transaction_id_start == transaction_id, "Other case not implemented yet"
      assert transaction_id_stop == transaction_id, "Other case not implemented yet"
      # TODO ack bitmap (for when transaction_id_start != transaction_id)
      ack_template = [ transaction_id_start, transaction_id_stop ]

    assert is_ack_recorded == False, "Not implemented yet"
    assert is_ack_not_void == False, "Not implemented yet"

    alp_command = AlpParser().parse(bitstream, payload_length)

    return Frame(control=control, dialog_id=dialog_id, transaction_id=transaction_id,
                 ack_template= ack_template, alp_command=alp_command)
