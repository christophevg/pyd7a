# operation.py
# author: Christophe VG <contact@christophe.vg>

# abstract base-class for operations

from abc import ABCMeta, abstractmethod, abstractproperty

class Operation(object):
  __metaclass__ = ABCMeta

  @abstractproperty
  def op(self): pass
