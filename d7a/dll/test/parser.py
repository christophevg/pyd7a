import unittest
import binascii
from PyCRC.CRCCCITT import CRCCCITT
from d7a.alp.operands.file import DataRequest, Data
from d7a.alp.operations.requests import RequestFileData
from d7a.alp.operations.responses import ReturnFileData

from d7a.dll.parser import Parser
from d7a.support.Crc import calculate_crc


class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()

  def test_read_id_command_frame(self):
    read_id_command = [
      0x15, # length
      0x00, # subnet
      0x00, # DLL control
      10, # D7ANP timeout
      0x20, # D7ANP control
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, # Origin Access ID
      0xc8, # D7ATP control
      0xe9, # dialog ID
      0x00, # transaction ID
      0x01, # ALP control (read file data operation)
      0x00, 0x00, 0x08, # file data request operand (file ID 0x00)
      0x08, 0x59 # CRC
    ]

    (frames, info) = self.parser.parse(read_id_command)
    self.assertEqual(len(frames), 1)
    frame = frames[0]
    self.assertEqual(frame.length, 21)
    self.assertEqual(frame.subnet, 0)
    self.assertFalse(frame.control.is_target_address_set, False)
    self.assertFalse(frame.control.is_target_address_vid, False)
    self.assertEqual(frame.control.eirp_index, 0)
    self.assertEqual(len(frame.target_address), 0)
    self.assertEqual(int(frame.d7anp_frame.timeout), 10)
    self.assertFalse(frame.d7anp_frame.control.has_network_layer_security)
    self.assertFalse(frame.d7anp_frame.control.has_multi_hop)
    self.assertTrue(frame.d7anp_frame.control.has_origin_access_id)
    self.assertFalse(frame.d7anp_frame.control.is_origin_access_id_vid)
    self.assertEqual(frame.d7anp_frame.control.origin_access_class, 0)
    self.assertEqual(frame.d7anp_frame.origin_access_id, [0, 0, 0, 0, 0, 0, 0, 1])
    self.assertFalse(frame.d7anp_frame.d7atp_frame.control.is_ack_recorded)
    self.assertTrue(frame.d7anp_frame.d7atp_frame.control.is_ack_return_template_requested)
    self.assertTrue(frame.d7anp_frame.d7atp_frame.control.is_dialog_end)
    self.assertTrue(frame.d7anp_frame.d7atp_frame.control.is_dialog_start)
    self.assertFalse(frame.d7anp_frame.d7atp_frame.control.is_ack_not_void)
    self.assertEqual(frame.d7anp_frame.d7atp_frame.dialog_id, 0xe9)
    self.assertEqual(frame.d7anp_frame.d7atp_frame.transaction_id, 0)
    self.assertEqual(len(frame.d7anp_frame.d7atp_frame.alp_command.actions), 1)
    alp_action = frame.d7anp_frame.d7atp_frame.alp_command.actions[0]
    self.assertEqual(type(alp_action.operation), RequestFileData)
    self.assertEqual(type(alp_action.operand), DataRequest)
    self.assertEqual(alp_action.operand.offset.id, 0)
    self.assertEqual(alp_action.operand.offset.offset, 0)
    self.assertEqual(alp_action.operand.length, 8)
    # TODO self.assertEqual(len(frame.payload), 16)
    hexstring = binascii.hexlify(bytearray(read_id_command[:-2])).decode('hex') # TODO there must be an easier way...
    self.assertEqual(frame.crc16, CRCCCITT(version='FFFF').calculate(hexstring))

  # TODO tmp
  def test_read_id_response_frame(self):
    frame_data = [ 0x25,  # length
                   0x00,  # subnet
                   0x80,  # dll control
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, # target_address
                   10, # D7ANP timeout
                   0x20,  # D7ANP control
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, # origin access ID
                   0x41,  # D7ATP control
                   0xe9,  # dialog ID
                   0x00,  # transaction ID
                   0x20,  # ALP control (return file data operation)
                   0x00, 0x00, 0x08, # file data operand
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, # UID
                   ]

    frame_data = frame_data + calculate_crc(frame_data)

    (frames, info) = self.parser.parse(frame_data)
    self.assertEqual(len(frames), 1)
    frame = frames[0]
    self.assertEqual(frame.length, 37)
    self.assertEqual(frame.subnet, 0)
    self.assertEqual(frame.control.is_target_address_set, True)
    self.assertEqual(frame.control.is_target_address_vid, False)
    self.assertEqual(frame.control.eirp_index, 0)
    self.assertEqual(len(frame.target_address), 8)
    self.assertEqual(frame.target_address, [0, 0, 0, 0, 0, 0, 0, 1])
    self.assertFalse(frame.d7anp_frame.control.has_network_layer_security)
    self.assertFalse(frame.d7anp_frame.control.has_multi_hop)
    self.assertTrue(frame.d7anp_frame.control.has_origin_access_id)
    self.assertFalse(frame.d7anp_frame.control.is_origin_access_id_vid)
    self.assertEqual(frame.d7anp_frame.control.origin_access_class, 0)
    self.assertEqual(frame.d7anp_frame.origin_access_id, [0, 0, 0, 0, 0, 0, 0, 2])
    self.assertFalse(frame.d7anp_frame.d7atp_frame.control.is_ack_recorded)
    self.assertFalse(frame.d7anp_frame.d7atp_frame.control.is_ack_return_template_requested)
    self.assertTrue(frame.d7anp_frame.d7atp_frame.control.is_dialog_end)
    self.assertFalse(frame.d7anp_frame.d7atp_frame.control.is_dialog_start)
    self.assertFalse(frame.d7anp_frame.d7atp_frame.control.is_ack_not_void)
    self.assertEqual(frame.d7anp_frame.d7atp_frame.dialog_id, 0xe9)
    self.assertEqual(frame.d7anp_frame.d7atp_frame.transaction_id, 0)
    self.assertEqual(len(frame.d7anp_frame.d7atp_frame.alp_command.actions), 1)
    alp_action = frame.d7anp_frame.d7atp_frame.alp_command.actions[0]
    self.assertEqual(type(alp_action.operation), ReturnFileData)
    self.assertEqual(type(alp_action.operand), Data)
    self.assertEqual(alp_action.operand.offset.id, 0)
    self.assertEqual(alp_action.operand.offset.offset, 0)
    self.assertEqual(alp_action.operand.length, 8)