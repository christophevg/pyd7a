from d7a.sp.status import Status
from d7a.support.schema import Validatable, Types


class FlushResultStatusOperand(Validatable):

  SCHEMA = [{
    "fifo_token"        : Types.BYTE(),
    "progess_bitmap"    : Types.BYTES(),
    "success_bitmap"    : Types.BYTES(),
    "bitmap_byte_size"  : Types.BYTE(),
  }]

  def __init__(self, fifo_token, progress_bitmap, success_bitmap, bitmap_byte_size):
    self.fifo_token = fifo_token
    self.progress_bitmap = progress_bitmap
    self.success_bitmap = success_bitmap
    self.bitmap_byte_size = bitmap_byte_size
    super(FlushResultStatusOperand, self).__init__()

  def __iter__(self):
    yield self.fifo_token
    yield self.bitmap_byte_size
    for byte in self.progress_bitmap: yield byte
    for byte in self.success_bitmap: yield byte

  def __str__(self):
    return "fifo-token={}, progress_bitmap={}, success_bitmap={}".format(
      self.fifo_token,
      self.progress_bitmap,
      self.success_bitmap
    )
