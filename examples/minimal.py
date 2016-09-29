#!/usr/bin/env python

from d7a.serial_console_interface.parser import Parser
from pprint import pprint

cmd = [
  0x20,                                   # action=32/ReturnFileData
  0x40,                                   # File ID
  0x00,                                   # offset
  0x04,                                   # length
  0x00, 0xf3, 0x00, 0x00                  # data
]
    
frame = [
  0xC0,                                   # interface sync byte
  0,                                      # interface version
  len(cmd),                               # ALP cmd length
] + cmd
    
(cmds, info) = Parser().parse(frame)

pprint(cmds[0].as_dict())

print([ "0x{:02x}".format(b) for b in bytearray(cmds[0]) ])
