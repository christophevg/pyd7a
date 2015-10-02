# responses.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for D7A ALP responses

import unittest
import sys

from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operands.file        import Data

class TestReturnFileData(unittest.TestCase):
  def test_constructor_and_op_code(self):
    data = Data([0x01, 0x02, 0x03, 0x04])
    rfd  = ReturnFileData(data)
    self.assertEqual(rfd.op, 32)
    self.assertIs(rfd.operand, data)
    self.assertEqual(rfd.operand.length, 4)
  
  def test_byte_generation(self):
    data  = Data([0x01, 0x02, 0x03, 0x04])
    rfd   = ReturnFileData(data)
    bytes = bytearray(rfd)
    self.assertEqual(len(bytes), 7)
    self.assertEqual(bytes[0], int('00000000', 2)) # offset
    self.assertEqual(bytes[1], int('00000000', 2)) # offset
    self.assertEqual(bytes[2], int('00000100', 2)) # length = 4
    self.assertEqual(bytes[3], int('00000001', 2))
    self.assertEqual(bytes[4], int('00000010', 2))
    self.assertEqual(bytes[5], int('00000011', 2))
    self.assertEqual(bytes[6], int('00000100', 2))

  def test_command_generation(self):
    data = list(bytearray("testing 123"))
    cmd  = ReturnFileData.send_command(
      addressee = 0x6666660000666666,
      file      = 0x66,
      data      = data
    )
    expected = [
      0xd7,                                           # interface start
      0x02, 0x02, 0x01, 0x03, 0x00, 0x00, 0x00,       # fifo config
      0x20,                                           # universal addr = 8 bytes
      0x66, 0x66, 0x66, 0x00, 0x00, 0x66, 0x66, 0x66, # ID
      0x20,                                           # action=32/ReturnFileData
      0x66,                                           # File ID
      0x00                                            # offset
    ]
    expected.append(len(data))
    expected.extend(data)
    bytes = bytearray(cmd)
    for i in xrange(len(expected)):
      self.assertEqual(bytes[i], expected[i])

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestNoOperation)
  unittest.TextTestRunner(verbosity=2).run(suite)
