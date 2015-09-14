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

To run unit tests we use `nose`:

```bash
$ sudo pip install nose
```

For the manipulation of bitstrings, we use `bitstring`:

```bash
$ sudo pip install bitstring
```

### pyD7A

Minimal survival commands:

```bash
$ git clone <location to be determined>
$ cd pyd7a
$ make
*** running all tests
.......................................................
----------------------------------------------------------------------
Ran 55 tests in 0.746s

OK
*** generating unittest coverage report (based on last test run)
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
d7a/alp/action                    14      0   100%   
d7a/alp/command                    9      0   100%   
d7a/alp/operands/file             18      0   100%   
d7a/alp/operations/nop             6      0   100%   
d7a/alp/operations/operation      12      0   100%   
d7a/alp/operations/responses       7      0   100%   
d7a/alp/parser                    75      2    97%   89-90
d7a/alp/payload                    7      0   100%   
d7a/sp/configuration              17      0   100%   
d7a/sp/qos                        13      0   100%   
d7a/sp/session                     9      0   100%   
d7a/sp/status                     16      0   100%   
d7a/tp/addressee                  19      0   100%   
d7a/types/ct                      11      0   100%   
------------------------------------------------------------
TOTAL                            233      2    99%
```

If all tests ran without any errors, you're good to go.

## Modules

TODO

### ALPParser

A parser for Application Layer Programming commands. From the specification: "_ALP is the D7A Application API. It is a generic API, optimized for usage with the D7A Session Protocol. It can be encapsulated in any other communication protocol. ALP defines a standard method to manage the Data Elements by the Application._"
