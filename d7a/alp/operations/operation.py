# operation.py
# author: Christophe VG <contact@christophe.vg>

# abstract base-class for operations

from abc import ABCMeta

from d7a.support.schema import Validatable

class Operation(Validatable):
  __metaclass__ = ABCMeta

  def __init__(self, operand=None):
    if self.operand_class is None and operand is not None:
      raise ValueError("{0} doesn't require an operand.".format(
                        self.__class__.__name__
                      ))
    if (operand is None and self.operand_class is not None) or \
       (operand is not None and not isinstance(operand, self.operand_class)):
      raise ValueError("{0} requires a {1} operand".format(
                        self.__class__.__name__,
                        self.operand_class.__name__
                      ))
    self.operand = operand
