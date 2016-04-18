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
    self.parser = Parser()
    self.interface_status_action = [
      51,                                             # Interface Status action
      0xD7,                                           # D7ASP interface
      0, 0, 0,                                        # channel_id
      0, 0,                                           # rssi
      0,                                              # link budget
      0,                                              # status
      0,                                              # fifo token
      0,                                              # request_id
      0,                                              # response timeout
      0                                               # addressee ctrl
    ]

  
  def test_basic_valid_message(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ] + self.interface_status_action

    cmd = self.parser.parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
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
    cmd = self.parser.parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
    self.assertEqual(cmd.actions[1].operation.op, 32)
    self.assertEqual(cmd.actions[1].operation.operand.length, 4)

  def test_command_without_interface_status(self):
    cmd_data = [
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
      # missing interface status action!
    ]
    cmd = self.parser.parse(ConstBitStream(bytes=cmd_data), len(cmd_data))
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
      cmd = self.parser.parse(ConstBitStream(bytes=cmd_data), len(cmd_data))

  def test_empty_data(self):
    alp_action_bytes = [
      0x20,
      0x40,
      0x00,
      0x00
    ] + self.interface_status_action

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

    cmd_bytes = alp_action_bytes + alp_action_bytes + self.interface_status_action
    cmd = self.parser.parse(ConstBitStream(bytes=cmd_bytes), len(cmd_bytes))
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
    cmd = self.parser.parse(ConstBitStream(bytes=cmd_bytes), len(cmd_bytes))

    self.assertEqual(len(cmd.actions), 3)
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
      51,                                             # action=51/Interface status
      0xd7,                                           # interface ID
      0x00, 0x00, 0x00,                               # channel_id
      0xc4, 0xff,                                     # RSSI
      0x00,                                           # link budget
      0x04,                                           # status
      0xa5,                                           # fifo token
      0x00,                                           # request ID
      0x00,                                           # response timeout
      0x20,                                           # addr control
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # addr
    ]
    cmd = self.parser.parse(ConstBitStream(bytes=alp_action_bytes), len(alp_action_bytes))

    self.assertEqual(len(cmd.actions), 1)
    self.assertEqual(cmd.actions[0].op, 51)
    self.assertEqual(type(cmd.actions[0].operand), InterfaceStatusOperand)
    self.assertEqual(cmd.actions[0].operand.interface_id, 0xD7)
    self.assertEqual(cmd.actions[0].operand.interface_status.channel_id, [0, 0, 0]) # TODO
    self.assertEqual(cmd.actions[0].operand.interface_status.rssi, -60)
    self.assertEqual(cmd.actions[0].operand.interface_status.link_budget, 0) # TODO
    self.assertEqual(cmd.actions[0].operand.interface_status.missed, False) # TODO
    self.assertEqual(cmd.actions[0].operand.interface_status.nls, False) # TODO
    self.assertEqual(cmd.actions[0].operand.interface_status.request_id, False) # TODO
    self.assertEqual(cmd.actions[0].operand.interface_status.response_to.exp, 0)
    self.assertEqual(cmd.actions[0].operand.interface_status.response_to.mant, 0)
    self.assertEqual(cmd.actions[0].operand.interface_status.retry, False)
    self.assertEqual(cmd.actions[0].operand.interface_status.state, 4) # TODO




  #def test_interface_status_action_unknown_interface(self):
    # TODO 

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParser)
  unittest.TextTestRunner(verbosity=2).run(suite)
