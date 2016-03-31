# parser.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP parser

import unittest

from pprint import pprint

from d7a.alp.parser import Parser

class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()
  
  def test_basic_valid_message(self):
    (cmds, info) = self.parser.parse([
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20,                                           # universal id = 8 bytes
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ])
    self.assertEqual(cmds[0].payload.actions[0].operation.op, 32)
    self.assertEqual(cmds[0].payload.actions[0].operation.operand.length, 4)

  def test_empty_data(self):
    (cmds, info) = self.parser.parse([
      0xd7,
      0x04, 0x00, 0x00, 0x00,
      0x20,
      0x24, 0x8a, 0xb6, 0x00, 0x52, 0x0b, 0x35, 0x2c,
      0x20,
      0x40,
      0x00,
      0x00
    ])
    self.assertEqual(cmds[0].payload.actions[0].operation.op, 32)
    self.assertEqual(len(cmds[0].payload.actions[0].operation.operand.data), 0)

  def test_bad_identifier(self):
    (cmds, info) = self.parser.parse([
      0x7d, # that's 7d not d7 ! ;-)
      0x04, 0x00, 0x00, 0x00,
      0x20,
      0x24, 0x8a, 0xb6, 0x00, 0x52, 0x0b, 0x35, 0x2c,
      0x20,
      0x40,
      0x00,
      0x00
    ])
    self.assertEquals(len(cmds), 0)
    self.assertEquals(len(info["errors"]), 1)

  def test_buffer_skipping(self):
    self.parser.buffer = [ 0x10, 0x20, 0x30, 0xd7, 0x10, 0x20, 0x30 ]
    skipped = self.parser.skip_bad_buffer_content()
    self.assertEquals(skipped, 3)
    self.assertEquals(self.parser.buffer, [ 0xd7, 0x10, 0x20, 0x30 ])

  def test_entire_buffer_skipping(self):
    self.parser.buffer = [ 0x10, 0x20, 0x30, 0x10, 0x20, 0x30 ]
    skipped = self.parser.skip_bad_buffer_content()
    self.assertEquals(skipped, 6)
    self.assertEquals(self.parser.buffer, [])

  def test_empty_buffer_skipping(self):
    self.parser.buffer = []
    skipped = self.parser.skip_bad_buffer_content()
    self.assertEquals(skipped, 0)
    self.assertEquals(self.parser.buffer, [])

  def test_buffer_skipping_with_first_item_the_id(self):
    self.parser.buffer = [ 0xd7, 0x10, 0x20, 0x30 ]
    skipped = self.parser.skip_bad_buffer_content()
    self.assertEquals(skipped, 4)
    self.assertEquals(self.parser.buffer, [])    

  def test_buffer_skipping_with_first_and_second_item_the_id(self):
    self.parser.buffer = [ 0xd7, 0xd7, 0x10, 0x20, 0x30 ]
    skipped = self.parser.skip_bad_buffer_content()
    self.assertEquals(skipped, 1)
    self.assertEquals(self.parser.buffer, [ 0xd7, 0x10, 0x20, 0x30 ])    

  def test_bad_identifier_with_identifier_in_body(self):
    (cmds, info) = self.parser.parse([
      0x7d, # that's 7d not d7 ! ;-)
      0x04, 0x00, 0x00, 0x00,
      0x20,
      0x24, 0x8a, 0xd7, 0x00, 0x52, 0x0b, 0x35, 0x2c,
      0x7d,       # ^ here's another one
      0x40,
      0x00,
      0x00
    ])
    self.assertEquals(len(cmds), 0)
    self.assertEquals(len(info["errors"]), 1)
    self.assertEquals(info["errors"][0]["skipped"], 8)

  def test_unsupported_action(self):
    (cmds, info) = self.parser.parse([
      0xd7,
      0x04, 0x00, 0x00, 0x00,
      0x20,
      0x24, 0x8a, 0xb6, 0x00, 0x52, 0x0b, 0x35, 0x2c,
      0x21,
      0x40,
      0x00,
      0x00
      ])
    self.assertEquals(len(cmds), 0)
    self.assertEquals(len(info["errors"]), 1)

  def test_partial_message(self):
    (cmds, info) = self.parser.parse([
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20                                            # addr (originally 0x00)
    ])
    self.assertEquals(len(cmds), 0)
    self.assertEquals(len(info["errors"]), 0)
    
  def test_continue_partial_message(self):
    self.test_partial_message()
    (cmds, info) = self.parser.parse([
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ])
    self.assertEqual(cmds[0].payload.actions[0].operation.op, 32)
    self.assertEqual(cmds[0].payload.actions[0].operation.operand.length, 4)

  def test_continue_from_bad_buffer(self):
    self.test_bad_identifier_with_identifier_in_body() # buffer is bad now
    self.test_basic_valid_message()                    # cont. with valid msg

  def test_multiple_commands(self):
    (cmds, info) = self.parser.parse([
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20,                                           # addr (originally 0x00)
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00,                         # data
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
    self.assertEqual(len(cmds), 2)
    self.assertEqual(cmds[0].payload.actions[0].operation.op, 32)
    self.assertEqual(cmds[0].payload.actions[0].operation.operand.length, 4)
    self.assertEqual(cmds[1].payload.actions[0].operation.op, 32)
    self.assertEqual(cmds[1].payload.actions[0].operation.operand.length, 4)

  def test_multiple_non_grouped_actions_in_command(self):
    (cmds, info) = self.parser.parse([
        0xd7,                                           # interface start
        0x04, 0x00, 0x00, 0x00,                         # fifo config
        0x20,                                           # addr (originally 0x00)
        0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
        0x20,                                           # action=32/ReturnFileData
        0x40,                                           # File ID
        0x00,                                           # offset
        0x04,                                           # length
        0x00, 0xf3, 0x00, 0x00,                         # data
        0x20,                                           # action=32/ReturnFileData
        0x40,                                           # File ID
        0x00,                                           # offset
        0x04,                                           # length
        0x00, 0xf3, 0x00, 0x00                          # data
    ])
    self.assertEqual(len(cmds), 1)
    self.assertEqual(len(cmds[0].payload.actions), 2)
    self.assertEqual(cmds[0].payload.actions[0].operation.op, 32)
    self.assertEqual(cmds[0].payload.actions[0].operation.operand.length, 4)
    self.assertEqual(cmds[0].payload.actions[1].operation.op, 32)
    self.assertEqual(cmds[0].payload.actions[1].operation.operand.length, 4)

  def test_multiple_grouped_actions_in_command(self):
    (cmds, info) = self.parser.parse([
        0xd7,                                           # interface start
        0x04, 0x00, 0x00, 0x00,                         # fifo config
        0x20,                                           # addr (originally 0x00)
        0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
        0xA0,                                           # action=32/ReturnFileData + grouped flag
        0x40,                                           # File ID
        0x00,                                           # offset
        0x04,                                           # length
        0x00, 0xf3, 0x00, 0x00,                         # data
        0x20,                                           # action=32/ReturnFileData
        0x40,                                           # File ID
        0x00,                                           # offset
        0x04,                                           # length
        0x00, 0xf3, 0x00, 0x00                          # data
    ])
    self.assertEqual(len(cmds), 1)
    self.assertEqual(len(cmds[0].payload.actions), 2)
    self.assertEqual(cmds[0].payload.actions[0].operation.op, 32)
    self.assertEqual(cmds[0].payload.actions[0].operation.operand.length, 4)
    self.assertEqual(cmds[0].payload.actions[0].group, True)
    self.assertEqual(cmds[0].payload.actions[1].operation.op, 32)
    self.assertEqual(cmds[0].payload.actions[1].operation.operand.length, 4)
    self.assertEqual(cmds[0].payload.actions[0].group, False)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
  unittest.TextTestRunner(verbosity=2).run(suite)
