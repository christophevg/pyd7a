# action.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ALP Action

import unittest

from d7a.alp.action         import Action
from d7a.alp.operations.nop import NoOperation

class TestAction(unittest.TestCase):
  def test_default_action_constructor(self):
    Action()
  
  def test_action_construction_switches(self):
    Action(group=True, resp=True)

  def test_default_nop_action_operand(self):
    a = Action()
    self.assertEqual(a.op, 0)

  def test_action_bad_operation(self):
    def bad(): Action(Action())
    self.assertRaises(ValueError, bad)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAction)
  unittest.TextTestRunner(verbosity=2).run(suite)
