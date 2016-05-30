import unittest

from d7a.alp.interface import InterfaceType
from d7a.alp.operands.interface_configuration import InterfaceConfiguration
from d7a.alp.operations.forward import Forward
from d7a.sp.configuration import Configuration


class TestForward(unittest.TestCase):
  def test_byte_generation(self):
    d7asp_config = Configuration()
    forward_action = Forward(
      operand=InterfaceConfiguration(
        interface_id=InterfaceType.D7ASP,
        interface_configuration=d7asp_config
      )
    )

    bytes = bytearray(forward_action)
    self.assertEqual(len(bytes), len(bytearray(d7asp_config)) + 1)
    self.assertEqual(bytes[0], 0xD7)
    self.assertEqual(bytes[1:], bytearray(d7asp_config))
    # TODO configuration
