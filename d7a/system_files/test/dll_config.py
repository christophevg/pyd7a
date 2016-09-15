import unittest

from bitstring import ConstBitStream

from d7a.system_files.dll_config import DllConfigFile


class TestDllConfigFile(unittest.TestCase):

  def test_default_constructor(self):
    c = DllConfigFile()
    self.assertEqual(c.active_access_class, 0)
    self.assertEqual(c.vid, 0xFFFF)

  def test_invalid_access_class(self):
    def bad(): DllConfigFile(active_access_class=21) # can be max 20
    self.assertRaises(ValueError, bad)

  def test_parsing(self):
    file_contents = [
      5,          # active access class
      0x00, 0x09  # VID
     ]

    config = DllConfigFile.parse(ConstBitStream(bytes=file_contents))
    self.assertEqual(config.active_access_class, 5)
    self.assertEqual(config.vid, 9)

  def test_byte_generation(self):
    bytes = bytearray(DllConfigFile())
    self.assertEqual(len(bytes), 3)
    self.assertEqual(bytes[0], 0)
    self.assertEqual(bytes[1], 0xFF)
    self.assertEqual(bytes[2], 0xFF)

    bytes = bytearray(DllConfigFile(active_access_class=5, vid=100))
    self.assertEqual(len(bytes), 3)
    self.assertEqual(bytes[0], 5)
    self.assertEqual(bytes[1], 0)
    self.assertEqual(bytes[2], 100)