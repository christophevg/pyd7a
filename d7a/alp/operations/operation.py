# operation.py
# author: Christophe VG <contact@christophe.vg>

# abstract base-class for operations

from abc import ABCMeta, abstractmethod, abstractproperty

class Operation(object):
  __metaclass__ = ABCMeta

  def __init__(self, operand=None):
    self.operand = operand

  @abstractproperty
  def op(self): pass
