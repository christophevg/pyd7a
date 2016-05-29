# parser
# author: Christophe VG <contact@christophe.vg>

# a parser for ALP commands wrapped in serial interface frames

from bitstring                    import ConstBitStream, ReadError
from d7a.alp.parser               import Parser as AlpParser
from d7a.parse_error              import ParseError


class Parser(object):

  def __init__(self):
    self.buffer = []

  def shift_buffer(self, start):
    self.buffer = self.buffer[start:]
    return self

  def parse(self, msg):
    self.buffer.extend(msg)
    return self.parse_buffer()

  @staticmethod
  def build_serial_frame(command):
    buffer = bytearray([ 'A', 'T', '$', 'D', 0xC0, 0 ])
    alp_command_bytes = bytearray(command)
    buffer.append(len(alp_command_bytes))
    buffer = buffer + alp_command_bytes
    return buffer

  def parse_buffer(self):
    parsed = 0
    cmds   = []

    while True:
      (cmd, info) = self.parse_one_command_from_buffer()
      if cmd is None: break
      parsed += info["parsed"]
      cmds.append(cmd)

    info["parsed"] = parsed
    return (cmds, info)

  def parse_one_command_from_buffer(self):
    retry       = True    # until we have one or don't have enough
    errors      = []
    cmd         = None
    bits_parsed = 0
    while retry and len(self.buffer) > 0:
      try:
        s           = ConstBitStream(bytes=self.buffer)
        cmd_length  = self.parse_serial_interface_header(s)
        cmd         = AlpParser().parse(s, cmd_length)
        bits_parsed = s.pos
        self.shift_buffer(bits_parsed/8)
        retry = False         # got one, carry on
      except ReadError:       # not enough to read, carry on and wait for more
        retry = False
      except ParseError as e: # actual problem with current buffer, need to skip
        errors.append({
          "error"   : e.args[0],
          "buffer"  : list(self.buffer),
          "pos"     : s.pos,
          "skipped" : self.skip_bad_buffer_content()
        })

    info = {
      "parsed" : bits_parsed,
      "buffer" : len(self.buffer) * 8,
      "errors" : errors
    }
    return (cmd, info)

  def skip_bad_buffer_content(self):
    # skip until we find 0xc0, which might be a valid starting point
    try:
      self.buffer.pop(0)                      # first might be 0xc0
      pos = self.buffer.index(0xc0)
      self.buffer = self.buffer[pos:]
      return pos + 1
    except IndexError:                        # empty buffer
      return 0
    except ValueError:                        # empty buffer, reported by .index
      skipped = len(self.buffer) + 1          # popped first item already
      self.buffer = []
      return skipped

  def parse_serial_interface_header(self, s):
      b = s.read("uint:8")
      if b != 0xC0 : raise ParseError("expected 0xC0, found {0}".format(b))
      version = s.read("uint:8")
      if version != 0: raise ParseError("Expected version 0, found {0}".format(version))
      cmd_len = s.read("uint:8")
      if len(self.buffer) - s.bytepos < cmd_len:
        raise ReadError("ALP command not complete yet, expected {0} bytes, got {1}".format(cmd_len, s.len - s.bytepos))

      return cmd_len

