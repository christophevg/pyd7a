# nop
# author: Christophe VG <contact@christophe.vg>

# class implementation of NoOperation

from d7a.alp.operations.operation import Operation

class NoOperation(Operation):

  NOP = 0
  OP  = NOP

  @property
  def op(self): return NoOperation.OP
