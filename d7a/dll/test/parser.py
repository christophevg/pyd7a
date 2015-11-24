import unittest
import binascii
from PyCRC.CRCCCITT import CRCCCITT

from d7a.dll.parser import Parser

class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()

  def test_basic_valid_frame(self):
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
    self.assertEqual(frame.control.is_target_address_set, False)
    self.assertEqual(frame.control.is_target_address_vid, False)
    self.assertEqual(frame.control.eirp_index, 0)
    self.assertEqual(len(frame.target_address), 0)
    self.assertEqual(len(frame.payload), 16)
    hexstring = binascii.hexlify(bytearray(read_id_command[:-2])).decode('hex') # TODO there must be an easier way...
    self.assertEqual(CRCCCITT(version='FFFF').calculate(hexstring), 0x1b3a)