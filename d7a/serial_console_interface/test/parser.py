# parser.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the serial interface parser

import unittest

from d7a.serial_console_interface.parser import Parser

class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()

  def test_basic_valid_message(self):
    alp_cmd_bytes = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]

    frame = [
      0xC0,                                           # interface sync byte
      0,                                              # interface version
      len(alp_cmd_bytes),                             # ALP cmd length
    ] + alp_cmd_bytes

    (cmds, info) = self.parser.parse(frame)
    self.assertEqual(cmds[0].actions[0].operation.op, 32)
    self.assertEqual(cmds[0].actions[0].operation.operand.length, 4)

  def test_bad_identifier(self):
    (cmds, info) = self.parser.parse([
      0x0c, # that's 0c not c0 ! ;-)
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
    self.parser.buffer = [ 0x10, 0x20, 0x30, 0xc0, 0x10, 0x20, 0x30 ]
    skipped = self.parser.skip_bad_buffer_content()
    self.assertEquals(skipped, 3)
    self.assertEquals(self.parser.buffer, [ 0xc0, 0x10, 0x20, 0x30 ])

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
    self.parser.buffer = [ 0xc0, 0x10, 0x20, 0x30 ]
    skipped = self.parser.skip_bad_buffer_content()
    self.assertEquals(skipped, 4)
    self.assertEquals(self.parser.buffer, [])

  def test_buffer_skipping_with_first_and_second_item_the_id(self):
    self.parser.buffer = [ 0xc0, 0xc0, 0x10, 0x20, 0x30 ]
    skipped = self.parser.skip_bad_buffer_content()
    self.assertEquals(skipped, 1)
    self.assertEquals(self.parser.buffer, [ 0xc0, 0x10, 0x20, 0x30 ])

  def test_bad_identifier_with_identifier_in_body(self):
    (cmds, info) = self.parser.parse([
      0x0c, # that's 0c not c0 ! ;-)
      0x04, 0x00, 0x00, 0x00,
      0x20,
      0x24, 0x8a, 0xc0, 0x00, 7, 0x0b, 0x35, 0x2c,
      0x7d,       # ^ here's another one
      0x40,
      0x00,
      0x00
    ])
    self.assertEquals(len(cmds), 0)
    self.assertEquals(len(info["errors"]), 2)
    self.assertEquals(info["errors"][0]["skipped"], 8)

  def test_partial_command(self):
    alp_action_bytes = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]

    (cmds, info) = self.parser.parse([
      0xc0,                                           # interface start
      0,
      2 * len(alp_action_bytes),                         # expect 2 ALP actions but only one in buffer
    ] + alp_action_bytes)
    self.assertEquals(len(cmds), 0)
    self.assertEquals(len(info["errors"]), 0)
    self.assertEquals(info["parsed"], 0)

  def test_continue_partial_command(self):
    self.test_partial_command() # incomplete command, add second ALP action to complete it ...
    (cmds, info) = self.parser.parse([
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ])
    self.assertEquals(len(info["errors"]), 0)
    self.assertEqual(len(cmds[0].actions), 2)


  def test_continue_from_bad_buffer(self):
    self.test_bad_identifier_with_identifier_in_body() # buffer is bad now
    self.test_basic_valid_message()                    # cont. with valid msg

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
  unittest.TextTestRunner(verbosity=2).run(suite)
