# Dash7 Python Support
A collection of Python modules, supporting Dash7.  
Christophe VG (<contact@christophe.vg>)

## Introduction

This repository contains a collection of Python modules that can help when working with the Dash7 Alliance Wireless Sensor and Actuator Network Protocol.

## Installation

### Dependencies

We use `Cerberus` for validating attributes. But we need a version &ge; 0.10, which is currently still a development version.

```bash
$ sudo pip install git+git://github.com/nicolaiarocci/cerberus.git
```

To run unit tests we use `unittest2`:

```bash
$ sudo pip install unittest2
```

And while we run tests, we check our coverage:

```bash
$ sudo pip install coverage
```

For the manipulation of bitstrings, we use `bitstring`:

```bash
$ sudo pip install bitstring
```

PyCRC is used for CRC calculations:

```bash
$ sudo pip install PyCRC
```

### pyD7A

Minimal survival commands:

```bash
$ git clone https://github.com/christophevg/pyd7a.git
$ cd pyd7a
$ make
*** running all tests
...................................................................
----------------------------------------------------------------------
Ran 67 tests in 0.967s

OK
*** generating unittest coverage report (based on last test run)
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
d7a/alp/action                    14      0   100%   
d7a/alp/command                    9      0   100%   
d7a/alp/operands/file             18      0   100%   
d7a/alp/operations/nop             6      0   100%   
d7a/alp/operations/operation      10      0   100%   
d7a/alp/operations/responses       7      0   100%   
d7a/alp/parser                   119      0   100%   
d7a/alp/payload                    7      0   100%   
d7a/sp/configuration              17      0   100%   
d7a/sp/qos                        13      0   100%   
d7a/sp/session                     9      0   100%   
d7a/sp/status                     16      0   100%   
d7a/tp/addressee                  19      0   100%   
d7a/types/ct                      11      0   100%   
------------------------------------------------------------
TOTAL                            275      0   100%
```

If all tests ran without any errors, you're good to go.

## Modules

### ALP Parser

A parser for Application Layer Programming commands. From the specification: "_ALP is the D7A Application API. It is a generic API, optimized for usage with the D7A Session Protocol. It can be encapsulated in any other communication protocol. ALP defines a standard method to manage the Data Elements by the Application._"

#### Minimal Example

```python
>>> from d7a.alp.parser import Parser
>>> bytes = [
...       0xd7,                                           # interface start
...       0x04, 0x00, 0x00, 0x00,                         # fifo config
...       0x20,                                           # addr (originally 0x00)
...       0x24, 0x8a, 0xb6, 0x01, 0x51, 0xc7, 0x96, 0x6d, # ID
...       0x20,                                           # action=32/ReturnFileData
...       0x40,                                           # File ID
...       0x00,                                           # offset
...       0x04,                                           # length
...       0x00, 0xf3, 0x00, 0x00                          # data
...     ]
>>> (cmds, info) = Parser().parse(bytes)
>>> from pprint import pprint
>>> pprint(cmds[0].as_dict())
{'__CLASS__': 'Command',
 'interface': {'__CLASS__': 'Status',
               'addressee': {'__CLASS__': 'Addressee',
                             'cl': 0,
                             'hasid': True,
                             'id': 2633117048934733421L,
                             'vid': False},
               'fifo_token': 0,
               'missed': False,
               'nls': False,
               'request_id': 0,
               'response_to': {'__CLASS__': 'CT', 'exp': 0, 'mant': 0},
               'retry': False,
               'state': 4},
 'payload': {'__CLASS__': 'Payload',
             'actions': [{'__CLASS__': 'Action',
                          'group': False,
                          'operation': {'__CLASS__': 'ReturnFileData',
                                        'op': 32,
                                        'operand': {'__CLASS__': 'Data',
                                                    'data': [0,
                                                             243,
                                                             0,
                                                             0],
                                                    'offset': {'__CLASS__': 'Offset',
                                                               'id': 64,
                                                               'offset': 0,
                                                               'size': 1}}},
                          'resp': False}]}}
```

#### Partial Parsing

The parser supports partial parsing and continues with previously unparsed data with consecutive calls. The `examples` folder contains an example called `partial.py` that illustrates this. The `parse()` method basically returns a list of commands it could parse from the currently assembled bytes.

#### Status

Currently the parser only implements the minimal constructions to parse `ReturnFileData` messages. The parser will be kept in sync with the supported messages in the [OSS-7: Open Source Stack for Dash7 Alliance Protocol](https://github.com/MOSAIC-LoPoW/dash7-ap-open-source-stack).

### ALP Message Generator

#### Minimal Example

```python
>>> bytes =
  [ 0xd7,   0x04,   0x00,   0x00,   0x00,   0x20,   0x24,
    0x8a,   0xb6,   0x01,   0x51,   0xc7,   0x96,   0x6d,
    0x20,   0x40,   0x00,   0x04,   0x00,   0xf3,   0x00,   0x00 ]
>>> (cmds, info) = Parser().parse(bytes)
>>> [ "0x{:02x}".format(b) for b in bytearray(cmds[0]) ]
  ['0xd7', '0x04', '0x00', '0x00', '0x00', '0x20', '0x24',
   '0x8a', '0xb6', '0x01', '0x51', '0xc7', '0x96', '0x6d',
   '0x20', '0x40', '0x00', '0x04', '0x00', '0xf3', '0x00', '0x00']
```

#### Tooling

```bash
$ cd examples/

$ ./generate_msg.py --help
usage: generate_msg.py [-h] [-v] [--hex] [-i]
                       addressee file data [more [more ...]]

tool to generate ALP messages

positional arguments:
  addressee      the addressee
  file           the file ID
  data           the file content
  more           the file content

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  be verbose
  --hex          display message in hex (default)
  -i, --int      display message in int

$ ./generate_msg.py 0x0102030405060708 0x55 "hello world"
0xd7 0x02 0x02 0x01 0x03 0x00 0x00 0x00 0x20 0x01 0x02 0x03 0x04 0x05 0x06 0x07 0x08 0x20 0x55 0x00 0x0b 0x68 0x65 0x6c 0x6c 0x6f 0x20 0x77 0x6f 0x72 0x6c 0x64 
```

#### Status

Currently the message generator only implements the minimal constructions to generate 'ReturnFileData' messages. The generator will be kept in sync with the parser.
