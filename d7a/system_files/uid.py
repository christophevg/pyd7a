import struct

from d7a.support.schema import Validatable, Types
from d7a.system_files.system_file_ids import SystemFileIds


class UidFile(Validatable):
  SCHEMA = [{
    "uid": Types.INTEGER(min=0, max=0xFFFFFFFFFFFFFFFF)
  }]

  def __init__(self, uid=0):
    self.uid = uid
    super(UidFile, self).__init__()

  def file_id(self):  # TODO base class
    return SystemFileIds.UID

  def length(self):  # TODO base class
    return 8 # TODO get from SCHEMA?

  @staticmethod
  def parse(s):
    uid = s.read("uint:64")
    return UidFile(uid=uid)

  def __iter__(self):
    for byte in bytearray(struct.pack(">Q", self.uid)):
      yield byte

