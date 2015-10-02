# generator.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP byte generators

import unittest

from d7a.alp.parser               import Parser

from d7a.alp.command              import Command
from d7a.alp.action               import Action
from d7a.alp.payload              import Payload

from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operands.file        import Data, Offset

from d7a.sp.status                import Status
from d7a.sp.session               import States

from d7a.tp.addressee             import Addressee

class TestGenerator(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()
  
  def test_basic_valid_message(self):
    msg = [
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20,                                           # addr (originally 0x00)
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]
    (cmds, info) = self.parser.parse(msg)
    bytes = bytearray(cmds[0])
    self.assertEqual(len(bytes), len(msg))
    for i in xrange(len(msg)):
      self.assertEqual(bytes[i], msg[i])

  def test_simple_return_file_data_command(self):
    cmd = Command(
      interface=Status(
        state=States.DONE,
        addressee=Addressee(id=0x0102030405)
      ),
      payload=Payload(
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
    )
    expected = [
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20,                                           # universal addr = 8 bytes
      0x00, 0x00, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, # ID
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
  suite = unittest.TestLoader().loadTestsFromTestCase(TestGenerator)
  unittest.TextTestRunner(verbosity=2).run(suite)
