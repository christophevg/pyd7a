import unittest

from d7a.alp.command import Command
from d7a.alp.operands.file import DataRequest, Offset, Data
from d7a.alp.operations.requests import ReadFileData
from d7a.alp.operations.write_operations import WriteFileData
from d7a.alp.regular_action import RegularAction


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
