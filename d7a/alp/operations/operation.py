# operation.py
# author: Christophe VG <contact@christophe.vg>

# abstract base-class for operations

from abc import ABCMeta, abstractmethod, abstractproperty

class Operation(object):
  __metaclass__ = ABCMeta

  def __init__(self, operand=None):
    if operand is not None and not isinstance(operand, self.OPERAND):
      raise ValueError("{0} requires a {1} operand".format(
                        self.__class__.__name__,
                        self.OPERAND.__name__
                      ))
    self.operand = operand

  @property
  def op(self): return self.OP
