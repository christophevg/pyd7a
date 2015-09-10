# operation.py
# author: Christophe VG <contact@christophe.vg>

# abstract base-class for operations

from abc import ABCMeta

class Operation(object):
  __metaclass__ = ABCMeta

  def __init__(self, operand=None):
    if self.OPERAND is None and operand is not None:
      raise ValueError("{0} doesn't require an operand.".format(
                        self.__class__.__name__
                      ))
    if (operand is None and self.OPERAND is not None) or \
       (operand is not None and not isinstance(operand, self.OPERAND)):
      raise ValueError("{0} requires a {1} operand".format(
                        self.__class__.__name__,
                        self.OPERAND.__name__
                      ))
    self.operand = operand

  @property
  def op(self): return self.OP
