import unittest
import binascii
from PyCRC.CRCCCITT import CRCCCITT

from d7a.dll.parser import Parser

class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()

  def test_read_id_command_frame(self):
    read_id_command = [
      0x14, # length
      0x00, # subnet
      0x00, # DLL control
      0x20, # D7ANP control
      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, # Origin Access ID
      0xc8, # D7ATP control
      0xe9, # dialog ID
      0x00, # transaction ID
      0x01, # ALP control (read file data operation)
      0x00, 0x00, 0x08, # file data request operand (file ID 0x00)
      0x1b, 0x3a # CRC
    ]

    (frames, info) = self.parser.parse(read_id_command)
    self.assertEqual(len(frames), 1)
    frame = frames[0]
    self.assertEqual(frame.length, 20)
    self.assertEqual(frame.subnet, 0)
    self.assertFalse(frame.control.is_target_address_set, False)
    self.assertFalse(frame.control.is_target_address_vid, False)
    self.assertEqual(frame.control.eirp_index, 0)
    self.assertEqual(len(frame.target_address), 0)
    self.assertFalse(frame.d7anp_frame.control.has_network_layer_security)
    self.assertFalse(frame.d7anp_frame.control.has_multi_hop)
    self.assertTrue(frame.d7anp_frame.control.has_origin_access_id)
    self.assertFalse(frame.d7anp_frame.control.is_origin_access_id_vid)
    self.assertEqual(frame.d7anp_frame.control.origin_access_class, 0)
    self.assertEqual(frame.d7anp_frame.origin_access_id, [0, 0, 0, 0, 0, 0, 0, 1])
    # TODO self.assertEqual(len(frame.payload), 16)
    hexstring = binascii.hexlify(bytearray(read_id_command[:-2])).decode('hex') # TODO there must be an easier way...
    self.assertEqual(frame.crc16, CRCCCITT(version='FFFF').calculate(hexstring))

  # TODO tmp
  def test_read_id_response_frame(self):
    frame_data = [ 0x25,  # length
                   0x00,  # subnet
                   0x80,  # dll control
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, # target_address
                   0x20,  # D7ANP control
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, # origin access ID
                   0x41,  # D7ATP control
                   0xe9,  # dialog ID
                   0x00,  # transaction ID
                   0x00,  # ACK template
                   0x20,  # ALP control (return file data operation)
                   0x00, 0x00, 0x08, # file data operand
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, # UID
                   0x5c, 0xb0 # CRC
                   ]

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
    # TODO self.assertEqual(len(frame.payload), 25)
    hexstring = binascii.hexlify(bytearray(frame_data[:-2])).decode('hex') # TODO there must be an easier way...
    self.assertEqual(frame.crc16, CRCCCITT(version='FFFF').calculate(hexstring))