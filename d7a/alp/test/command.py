# command.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP command byte generation

import unittest

from d7a.alp.parser               import Parser

from d7a.alp.command              import Command
from d7a.alp.action               import Action
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operands.file        import Data, Offset


class TestCommand(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()

  def test_simple_received_return_file_data_command(self):
    cmd = Command(
        actions=[
          Action(
            operation=ReturnFileData(
              operand=Data(
                data=list(bytearray("Hello world")),
                offset=Offset(id=0x51)
              )
            )
          )
        ]
    )
    expected = [
      0x20,                                           # action=32/ReturnFileData
      0x51,                                           # File ID
      0x00,                                           # offset
      0x0b,                                           # length
      0x48, 0x65, 0x6c, 0x6c, 0x6f,                   # Hello
      0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64              # World
    ]
    bytes = bytearray(cmd)
    for i in xrange(len(expected)):
      self.assertEqual(bytes[i], expected[i])

  def test_simple_send_return_file_data_command(self):
    cmd = Command(
      actions=[
        Action(
          operation=ReturnFileData(
            operand=Data(
              data=list(bytearray("Hello world")),
              offset=Offset(id=0x51)
            )
          )
        )
      ]
    )
    expected = [
      0x20,                                           # action=32/ReturnFileData
      0x51,                                           # File ID
      0x00,                                           # offset
      0x0b,                                           # length
      0x48, 0x65, 0x6c, 0x6c, 0x6f,                   # Hello
      0x20, 0x77, 0x6f, 0x72, 0x6c, 0x64              # World
    ]
    bytes = bytearray(cmd)
    for i in xrange(len(expected)):
      self.assertEqual(bytes[i], expected[i])

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCommand)
  unittest.TextTestRunner(verbosity=2).run(suite)
