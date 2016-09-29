#!/usr/bin/env python

# command line tool to generate ALP messages
# author: Christophe VG <contact@christophe.vg>

import sys
import argparse

from d7a.alp.operations.responses import ReturnFileData

def generate_message(operation, addressee, file, data):
  return bytearray(
    operation.send_command(
      addressee = addressee,
      file      = file,
      data      = data
  ))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="tool to generate ALP messages"
  )

  parser.add_argument("-v", "--verbose", help="be verbose",
                      action='store_true', default=False)
  parser.add_argument("--hex", dest="style",
                      help="display message in hex (default)",
                      action="store_const", const=hex, default=hex)
  parser.add_argument("-i", "--int", dest="style",
                      help="display message in int",
                      action="store_const", const=int)

  def unknown_int(val): return int(val, 0)

  parser.add_argument("addressee", help="the addressee",    type=unknown_int)
  parser.add_argument("file",      help="the file ID",      type=unknown_int)
  parser.add_argument("data",      help="the file content")
  parser.add_argument("more",      help="the file content", nargs="*")
  
  config = parser.parse_args()

  if config.more != []:
    data = [unknown_int(config.data)]
    data.extend(map(unknown_int, config.more))
  else:
    data =  list(bytearray(config.data))

  cmd = generate_message(
    ReturnFileData,
    config.addressee,
    config.file,
    data
  )

  bytes = list(bytearray(cmd))
  if config.verbose:
    print "message size =", len(bytes)

  if config.style == hex:
    [ sys.stdout.write("0x{:02x} ".format(b)) for b in bytes ]
    print
  elif config.style == int:
    print bytes
  