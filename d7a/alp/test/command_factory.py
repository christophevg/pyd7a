import unittest

from d7a.alp.command import Command
from d7a.alp.operands.file import DataRequest, Offset
from d7a.alp.operations.requests import ReadFileData
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
