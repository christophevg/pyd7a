# parser.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP parser

import unittest

from bitstring import ConstBitStream
from d7a.alp.operands.interface_status import InterfaceStatusOperand

from d7a.alp.parser import Parser
from d7a.parse_error import ParseError


class TestParser(unittest.TestCase):
  def setUp(self):
    self.interface_status_action = [
      0x62,                                           # Interface Status action
      0xD7,                                           # D7ASP interface
      0,                                              # channel_header
      0, 0,                                           # channel_id
      0,                                              # rxlevel (- dBm)
      0,                                              # link budget
      0,                                              # status
      0,                                              # fifo token
      0,                                              # seq
      0,                                              # response timeout
      16                                              # addressee ctrl (BCAST)
    ]

  def test_basic_valid_message(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ] + self.interface_status_action

    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length, 4)

  def test_basic_valid_message_actions_swapped(self):
    cmd_data = self.interface_status_action + [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]
    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(cmd.actions[0].operation.op, 32)
    self.assertEqual(cmd.actions[0].operation.operand.length, 4)

  def test_command_without_interface_status(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xfF, 0x00, 0x00                          # data
      # missing interface status action!
    ]
    cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(cmd.interface_status, None)

  def test_command_with_multiple_interface_status_actions(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ] + self.interface_status_action + self.interface_status_action # <- 2x interface_status!
    with self.assertRaises(ParseError):
      cmd = Parser().parse(ConstBitStream(bytes=cmd_data), len(cmd_data))

  def test_empty_data(self):
    alp_action_bytes = [
      0x20,
      0x40,
      0x00,
      0x00
    ]

    parser = Parser()
    cmd = parser.parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))
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
      cmd = Parser().parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))

  def test_multiple_actions(self):
    alp_action_bytes = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00,                         # data
    ]

    cmd_bytes = alp_action_bytes + alp_action_bytes + self.interface_status_action
    cmd = Parser().parse(ConstBitStream(bytes=cmd_bytes), len(cmd_bytes))
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

    cmd_bytes = alp_action_bytes + alp_action_bytes + self.interface_status_action
    cmd = Parser().parse(ConstBitStream(bytes=cmd_bytes), len(cmd_bytes))

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

  def test_interface_status_action_d7asp(self):
    alp_action_bytes = [
      0x62,                                           # action=51/Interface status
      0xd7,                                           # interface ID
      0x00,                                           # channel_header
      16, 0,                                          # channel_index
      70,                                             # rx level
      80,                                             # link budget
      0,                                              # status
      0xa5,                                           # fifo token
      0x00,                                           # request ID
      20,                                             # response timeout
      0x20,                                           # addr control
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # addr
    ]

    cmd = Parser().parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))
    self.assertIsNotNone(cmd.interface_status)
    self.assertEqual(cmd.interface_status.op, 34)
    self.assertEqual(type(cmd.interface_status.operand), InterfaceStatusOperand)
    self.assertEqual(cmd.interface_status.operand.interface_id, 0xD7)
    self.assertEqual(cmd.interface_status.operand.interface_status.channel_header, 0) # TODO
    self.assertEqual(cmd.interface_status.operand.interface_status.channel_index, 16)
    self.assertEqual(cmd.interface_status.operand.interface_status.rx_level, 70)
    self.assertEqual(cmd.interface_status.operand.interface_status.link_budget, 80)
    self.assertEqual(cmd.interface_status.operand.interface_status.missed, False)
    self.assertEqual(cmd.interface_status.operand.interface_status.nls, False)
    self.assertEqual(cmd.interface_status.operand.interface_status.seq_nr, 0)
    self.assertEqual(cmd.interface_status.operand.interface_status.response_to.exp, 0)
    self.assertEqual(cmd.interface_status.operand.interface_status.response_to.mant, 20)
    self.assertEqual(cmd.interface_status.operand.interface_status.retry, False)



  #def test_interface_status_action_unknown_interface(self):
    # TODO 

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
  unittest.TextTestRunner(verbosity=2).run(suite)
