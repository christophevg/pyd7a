import struct
import unittest
from bitstring import ConstBitStream
from d7a.system_files.uid import UidFile


class TestUiFile(unittest.TestCase):

  def test_default_constructor(self):
    f = UidFile()
    self.assertEqual(f.uid, 0)

  def test_constructor(self):
    uid = 0xDEADBEEF
    f = UidFile(uid=uid)
    self.assertEqual(f.uid, uid)

  def test_invalid_id(self):
    def bad(): UidFile(uid=-1)
    self.assertRaises(ValueError, bad)

  def test_parsing(self):
    file_contents = [
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09  # UID
     ]

    config = UidFile.parse(ConstBitStream(bytes=file_contents))
    self.assertEqual(config.uid, 9)

  def test_byte_generation(self):
    uid = 12345
    bytes = bytearray(UidFile(uid))
    self.assertEqual(len(bytes), 8)
    self.assertEqual(struct.unpack(">Q", bytes)[0], uid)
