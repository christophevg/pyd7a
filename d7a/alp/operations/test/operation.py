# operation.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the Operation base class

import unittest

from d7a.alp.operations.operation import Operation

class OperandX(object): pass
class OperandY(object): pass

def make_operation(operand=None, op=None):
  class MyOperation(Operation):
    def __init__(self, *args, **kwargs):
      self.OPERAND = operand
      self.OP      = op
      super(MyOperation, self).__init__(*args, **kwargs)
  return MyOperation

class TestOperation(unittest.TestCase):
  
  def test_not_implemented_operand(self):
    def bad(): Operation()
    self.assertRaises(AttributeError, bad)

  def test_missing_operand(self):
    MyOperation = make_operation(operand=OperandX)
    def bad(): MyOperation()
    self.assertRaises(ValueError, bad)

  def test_unexpected_operand(self):
    MyOperation = make_operation()
    def bad(): MyOperation(OperandY())
    self.assertRaises(ValueError, bad)
    

  def test_incorrect_operand(self):
    MyOperation = make_operation(operand=OperandX)
    def bad(): MyOperation(OperandY())
    self.assertRaises(ValueError, bad)

  def test_op_property(self):
    MyOperation = make_operation(operand=None, op=123)
    op = MyOperation()
    self.assertEquals(op.op, 123)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestOperation)
  unittest.TextTestRunner(verbosity=2).run(suite)
