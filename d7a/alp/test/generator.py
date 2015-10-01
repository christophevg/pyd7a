# generator.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP byte generators

import unittest

from pprint import pprint

from d7a.alp.parser import Parser

class TestGenerator(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()
  
  def test_basic_valid_message(self):
    msg = [
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20,                                           # addr (originally 0x00)
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]
    (cmds, info) = self.parser.parse(msg)
    bytes = bytearray(cmds[0])
    self.assertEqual(len(bytes), len(msg))
    for i in xrange(len(msg)):
      self.assertEqual(bytes[i], msg[i])

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestGenerator)
  unittest.TextTestRunner(verbosity=2).run(suite)
