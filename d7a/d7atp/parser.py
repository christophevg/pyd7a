
from bitstring import ConstBitStream, ReadError
from d7a.d7atp.frame import Frame
from d7a.d7atp.control import Control
from d7a.alp.parser import Parser as AlpParser

class Parser(object):

  def parse(self, bitstream, payload_length):
    is_dialog_start = bitstream.read("bool")
    is_dialog_end = bitstream.read("bool")
    has_timeout_template = bitstream.read("bool")
    _=bitstream.read("pad:1"),
    is_ack_return_template_requested = bitstream.read("bool")
    should_respond_only_if_act_return_template_not_empty = bitstream.read("bool")
    is_ack_recorded = bitstream.read("bool")
    has_ack_template = bitstream.read("bool")
    payload_length = payload_length - 1 # subtract control byte

    control = Control(is_dialog_start, is_dialog_end, has_timeout_template, is_ack_return_template_requested,
                      should_respond_only_if_act_return_template_not_empty, is_ack_recorded, has_ack_template)

    dialog_id = bitstream.read("uint:8")
    payload_length = payload_length - 1

    transaction_id = bitstream.read("uint:8")
    payload_length = payload_length - 1

    timeout_template = None
    if has_timeout_template:
      timeout_template = bitstream.read("uint:8")
      payload_length = payload_length - 1

    ack_template = None
    if has_ack_template:
      transaction_id_start = bitstream.read("uint:8")
      payload_length = payload_length - 1
      assert transaction_id_start == transaction_id, "Other case not implemented yet"
      # TODO ack bitmap (for when transaction_id_start != transaction_id)
      ack_template = [ transaction_id_start ]

    assert is_ack_recorded == False, "Not implemented yet"
    assert should_respond_only_if_act_return_template_not_empty == False, "Not implemented yet"

    alp_command = AlpParser().parse(bitstream, payload_length)

    return Frame(control=control, dialog_id=dialog_id, transaction_id=transaction_id,
                 timeout_template=timeout_template, ack_template= ack_template, alp_command=alp_command)
