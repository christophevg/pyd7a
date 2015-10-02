#!/usr/bin/env PYTHONPATH=../:. python

from pprint import pprint

from d7a.alp.parser import Parser

part1 = [
      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00,                         # fifo config
      0x20,                                           # addressee
      0x24, 0x8a, 0xb6 
]

part2 = [
                       0x01, 0x51, 0xc7, 0x96, 0x6d,  # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x04,                                           # length
      0x00, 0xf3, 0x00, 0x00,                         # data

      0xd7,                                           # interface start
      0x04, 0x00, 0x00, 0x00                          # fifo config
]

part3 = [
      0x20,                                           # addressee
      0x24, 0x8a, 0xb6, 0x00, 0x52, 0x0b, 0x35, 0x2c, # ID
      0x20,                                           # action=32/ReturnFileData
      0x40,                                           # File ID
      0x00,                                           # offset
      0x00                                            # length
    ]

parser = Parser()

(cmds, info) = parser.parse(part1)
pprint(info)
for cmd in cmds: pprint(cmd.as_dict())

(cmds, info) = parser.parse(part2)
pprint(info)
for cmd in cmds: pprint(cmd.as_dict())

(cmds, info) = parser.parse(part3)
pprint(info)
for cmd in cmds: pprint(cmd.as_dict())
