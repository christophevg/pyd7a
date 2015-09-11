# parser.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP parser

import unittest

from pprint import pprint

from d7a.alp.parser import Parser

class TestParser(unittest.TestCase):
  def test_first_msg_from_glenn(self):
    p = Parser()
    result = p.parse([
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20,                                           # addr (originally 0x00)
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ])

    # parsing errors reported?
    if result["_error"]: self.fail("parsing error")

    # full parse?
    self.assertEqual(result["_stream"]["len"], result["_stream"]["pos"])

    # correct operation
    self.assertEqual(result["opcode"], 32)
    
    # correct data length?

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
  unittest.TextTestRunner(verbosity=2).run(suite)
