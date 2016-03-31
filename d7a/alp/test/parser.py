# parser.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP parser

import unittest

from bitstring import ConstBitStream

from d7a.alp.parser import Parser
from d7a.parse_error import ParseError


class TestParser(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()
  
  def test_basic_valid_message(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]
    cmd = self.parser.parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length, 4)

  def test_empty_data(self):
    alp_action_bytes = [
      0x20,
      0x40,
      0x00,
      0x00
    ]

    cmd = self.parser.parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(len(cmd.actions[0].operation.operand.data), 0)

  def test_unsupported_action(self):
    alp_action_bytes = [
      0x21,
      0x40,
      0x00,
      0x00
    ]
    with self.assertRaises(ParseError):
      cmd = self.parser.parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))

  def test_multiple_actions(self):
    alp_action_bytes = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00,                         # data
    ]

    cmd = self.parser.parse(ConstBitStream(bytes=(alp_action_bytes + alp_action_bytes)),
                                                    2 * len(alp_action_bytes))
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length, 4)
    self.assertEqual(cmd.actions[1].operation.op, 32)
    self.assertEqual(cmd.actions[1].operation.operand.length, 4)

  def test_multiple_non_grouped_actions_in_command(self):
    alp_action_bytes = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]
    cmd = self.parser.parse(ConstBitStream(bytes=alp_action_bytes + alp_action_bytes), 2 * len(alp_action_bytes))

    self.assertEqual(len(cmd.actions), 2)
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length, 4)
    self.assertEqual(cmd.actions[1].operation.op, 32)
    self.assertEqual(cmd.actions[1].operation.operand.length, 4)

  # TODO not implemented yet
  # def test_multiple_grouped_actions_in_command(self):
  #   alp_action_first_in_group_bytes = [
  #     0xa0,                                           # action=32/ReturnFileData  + grouped flag
  #     0x40,                                           # File ID
  #     0x00,                                           # offset
  #     0x04,                                           # length
  #     0x00, 0xf3, 0x00, 0x00                          # data
  #   ]
  #   alp_action_second_in_group_bytes = [
  #     0x20,                                           # action=32/ReturnFileData
  #     0x40,                                           # File ID
  #     0x00,                                           # offset
  #     0x04,                                           # length
  #     0x00, 0xf3, 0x00, 0x00                          # data
  #   ]
  #   (cmds, info) = self.parser.parse([
  #     0xc0, 0, len(alp_action_first_in_group_bytes) + len(alp_action_second_in_group_bytes)
  #   ] + alp_action_first_in_group_bytes + alp_action_second_in_group_bytes)
  #
  #   self.assertEqual(len(cmds), 1)
  #   self.assertEqual(len(cmds[0].actions), 2)
  #   self.assertEqual(cmds[0].actions[0].operation.op, 32)
  #   self.assertEqual(cmds[0].actions[0].operation.operand.length, 4)
  #   self.assertEqual(cmds[0].actions[0].group, True)
  #   self.assertEqual(cmds[0].actions[1].operation.op, 32)
  #   self.assertEqual(cmds[0].actions[1].operation.operand.length, 4)
  #   self.assertEqual(cmds[0].actions[0].group, False)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
  unittest.TextTestRunner(verbosity=2).run(suite)
