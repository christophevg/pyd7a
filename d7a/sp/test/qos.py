# qos.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7A SP QoS Paramters 

import unittest

from d7a.sp.qos import QoS

class TestQoS(unittest.TestCase):
  def test_default_constructor(self):
    qos = QoS()

  def test_byte_generation(self):
    bytes = bytearray(QoS())
    self.assertEqual(len(bytes), 1)
    self.assertEqual(bytes[0], int('00000000', 2))

    bytes = bytearray(QoS(
      nls= True,
      resp_mod    = QoS.RESP_MODE_ANY,
      record=True,
      stop_on_err=True,
    ))
    self.assertEqual(len(bytes), 1)
    self.assertEqual(bytes[0], int('11100010', 2))

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestQoS)
  unittest.TextTestRunner(verbosity=2).run(suite)
