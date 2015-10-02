#!/usr/bin/env PYTHONPATH=../:. python

from d7a.alp.parser import Parser
from pprint import pprint

bytes = [
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20,                                           # addr (originally 0x00)
      0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00                          # data
    ]

(cmds, info) = Parser().parse(bytes)

pprint(cmds[0].as_dict())

print([ "0x{:02x}".format(b) for b in bytearray(cmds[0]) ])
