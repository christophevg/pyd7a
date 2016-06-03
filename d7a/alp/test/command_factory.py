import unittest
import binascii

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.alp.operands.file import DataRequest, Offset, Data
from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.alp.operations.forward import Forward
from d7a.alp.operations.requests import ReadFileData
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operations.write_operations import WriteFileData
from d7a.alp.regular_action import RegularAction
from d7a.sp.configuration import Configuration


class TestCommandFactory(unittest.TestCase):
  def test_create_with_read_file_action(self):
    c = Command.create_with_read_file_action(file_id=1, length=10)
    self.assertEqual(len(c.actions), 1)
    self.assertEqual(type(c.actions[0]), RegularAction)
    self.assertEqual(type(c.actions[0].operation), ReadFileData)
    self.assertEqual(type(c.actions[0].operand), DataRequest)
    self.assertEqual(c.actions[0].operand.offset.id, 1)
    self.assertEqual(c.actions[0].operand.offset.size, 1)
    self.assertEqual(c.actions[0].operand.offset.offset, 0)
    self.assertEqual(c.actions[0].operand.length, 10)

  def test_create_with_write_file_action(self):
    data = [0, 1, 2, 3, 4, 5]
    c = Command.create_with_write_file_action(file_id=1, data=data)
    self.assertEqual(len(c.actions), 1)
    self.assertEqual(type(c.actions[0]), RegularAction)
    self.assertEqual(type(c.actions[0].operation), WriteFileData)
    self.assertEqual(type(c.actions[0].operand), Data)
    self.assertEqual(c.actions[0].operand.offset.id, 1)
    self.assertEqual(c.actions[0].operand.offset.size, 1)
    self.assertEqual(c.actions[0].operand.offset.offset, 0)
    self.assertEqual(c.actions[0].operand.length, 6)
    self.assertEqual(c.actions[0].operand.data, data)

  def test_create_with_return_file_data_action(self):
    data = [ 1 ]
    c = Command.create_with_return_file_data_action(file_id=0x40, data=data)
    self.assertEqual(len(c.actions), 1)
    self.assertEqual(type(c.actions[0]), RegularAction)
    self.assertEqual(type(c.actions[0].operation), ReturnFileData)
    self.assertEqual(type(c.actions[0].operand), Data)
    self.assertEqual(c.actions[0].operand.offset.id, 0x40)
    self.assertEqual(c.actions[0].operand.offset.size, 1)
    self.assertEqual(c.actions[0].operand.offset.offset, 0)
    self.assertEqual(c.actions[0].operand.length, 1)
    self.assertEqual(c.actions[0].operand.data, data)

  def test_create_with_read_file_action_d7asp(self):
    c = Command.create_with_read_file_action(file_id=1, length=10, interface_type=InterfaceType.D7ASP)
    self.assertEqual(len(c.actions), 2)
    self.assertEqual(type(c.actions[0]), RegularAction)
    self.assertEqual(type(c.actions[0].operation), Forward)
    self.assertEqual(type(c.actions[0].operand), InterfaceConfiguration)
    self.assertEqual(c.actions[0].operand.interface_id, 0xD7)
    self.assertEqual(type(c.actions[0].operand.interface_configuration), Configuration)
    # TODO configuration properties
    self.assertEqual(type(c.actions[1].operation), ReadFileData)
    self.assertEqual(type(c.actions[1].operand), DataRequest)
    self.assertEqual(type(c.actions[1]), RegularAction)
    self.assertEqual(type(c.actions[1].operation), ReadFileData)
    self.assertEqual(type(c.actions[1].operand), DataRequest)
    self.assertEqual(c.actions[1].operand.offset.id, 1)
    self.assertEqual(c.actions[1].operand.offset.size, 1)
    self.assertEqual(c.actions[1].operand.offset.offset, 0)
    self.assertEqual(c.actions[1].operand.length, 10)

  def test_create_with_write_file_action_d7asp(self):
    data = [0, 1, 2, 3, 4, 5]
    c = Command.create_with_write_file_action(file_id=1, data=data, interface_type=InterfaceType.D7ASP)
    self.assertEqual(len(c.actions), 2)
    self.assertEqual(type(c.actions[0]), RegularAction)
    self.assertEqual(type(c.actions[0].operation), Forward)
    self.assertEqual(type(c.actions[0].operand), InterfaceConfiguration)
    self.assertEqual(c.actions[0].operand.interface_id, 0xD7)
    self.assertEqual(type(c.actions[0].operand.interface_configuration), Configuration)
    # TODO configuration properties
    self.assertEqual(type(c.actions[1].operation), WriteFileData)
    self.assertEqual(type(c.actions[1].operand), Data)
    self.assertEqual(c.actions[1].operand.offset.id, 1)
    self.assertEqual(c.actions[1].operand.offset.size, 1)
    self.assertEqual(c.actions[1].operand.offset.offset, 0)
    self.assertEqual(c.actions[1].operand.length, 6)
    self.assertEqual(c.actions[1].operand.data, data)

  def test_create_with_return_file_data_action_d7asp(self):
    data = [1]
    c = Command.create_with_return_file_data_action(file_id=0x40, data=data, interface_type=InterfaceType.D7ASP)
    self.assertEqual(len(c.actions), 2)
    self.assertEqual(type(c.actions[0]), RegularAction)
    self.assertEqual(type(c.actions[0].operation), Forward)
    self.assertEqual(type(c.actions[0].operand), InterfaceConfiguration)
    self.assertEqual(c.actions[0].operand.interface_id, 0xD7)
    self.assertEqual(type(c.actions[0].operand.interface_configuration), Configuration)
    self.assertEqual(type(c.actions[1]), RegularAction)
    self.assertEqual(type(c.actions[1].operation), ReturnFileData)
    self.assertEqual(type(c.actions[1].operand), Data)
    self.assertEqual(c.actions[1].operand.offset.id, 0x40)
    self.assertEqual(c.actions[1].operand.offset.size, 1)
    self.assertEqual(c.actions[1].operand.offset.offset, 0)
    self.assertEqual(c.actions[1].operand.length, 1)
    self.assertEqual(c.actions[1].operand.data, data)
