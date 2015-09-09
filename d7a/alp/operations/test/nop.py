# nop.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP NoOperation

import unittest

from d7a.alp.operations.nop import NoOperation

class TestNoOperation(unittest.TestCase):
  def test_constructor_and_op_code(self):
    nop = NoOperation()
    self.assertEqual(nop.op, 0)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestNoOperation)
  unittest.TextTestRunner(verbosity=2).run(suite)
