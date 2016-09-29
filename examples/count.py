#!/usr/bin/env python

import argparse
import serial
import random
import time

from d7a.serial_console_interface.parser import Parser
from pprint import pprint

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS
from d7a.system_files.uid import UidFile
from modem.modem import Modem

argparser = argparse.ArgumentParser()

argparser.add_argument("-s", "--serial", help="serial device /dev file", 
                       default="/dev/tty.usbserial-FTGCT0HY")
argparser.add_argument("-b", "--baudrate", help="baudrate for serial device", 
                       type=int, default=115200)

config = argparser.parse_args()

modem = Modem(config.serial, config.baudrate, show_logging=False)

cmd = Command.create_with_return_file_data_action(
    file_id=0x40,
    data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    interface_type=InterfaceType.D7ASP,
    interface_configuration=Configuration(
      qos=QoS(resp_mod=QoS.RESP_MODE_NO),
      addressee=Addressee(
        access_class=0,
        id_type=IdType.BCAST
      )
    )
  )

last_message = 0

sent = 0
received = 0

def stats():
	print "sent", sent, "received", received

while True:
  # Read from D7 modem and decode packets/commands
  (cmds, info) = modem.read()
  if len(info["errors"]) < 1:
    if len(cmds) > 0:
			received += 1
			stats()
  else:
    pprint(info)
  
  # every second, at random, send a message
  now = round(time.time())
  if last_message < now:
    last_message = now
    if random.random() > 0.50:
      modem.d7asp_fifo_flush(alp_command=cmd)
      sent += 1
      stats()