# parser.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP parser

import unittest

from pprint import pprint

from d7a.alp.parser import Parser

class TestParser(unittest.TestCase):
  def parse_message(self, message):
    (msg, info) = Parser().parse(message)

    # full parse?
    self.assertEqual(info["stream"]["len"], info["stream"]["pos"])

    return (msg, info)
    
  def test_first_msg_from_glenn(self):
    (msg, info) = self.parse_message([
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
    self.assertEqual(msg.payload.actions[0].operation.OP, 32)
    self.assertEqual(msg.payload.actions[0].operation.operand.length, 4)

  def test_empty_data(self):
    (msg, info) = self.parse_message([
      0xd7,
      0x04, 0x00, 0x00, 0x00,
      0x20,
      0x24, 0x8a, 0xb6, 0x00, 0x52, 0x0b, 0x35, 0x2c,
      0x20,
      0x40,
      0x00,
      0x00
    ])
    self.assertEqual(msg.payload.actions[0].operation.OP, 32)
    self.assertEqual(len(msg.payload.actions[0].operation.operand.data), 0)

# 00000000: d7 04 00 00 00 20 24 8a   b6 00 52 0b 35 2c 20 40
# 00000010: 00 04 00 fa 00 00

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
  unittest.TextTestRunner(verbosity=2).run(suite)
