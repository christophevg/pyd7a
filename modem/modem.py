#!/usr/bin/env python
import argparse
import time
import serial

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.serial_console_interface.parser import Parser
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS


class Modem:
  def __init__(self, serial_device, serial_rate):
    self.setup_serial_device(serial_device, serial_rate)
    self.parser = Parser()

  def setup_serial_device(self, serial_device, serial_rate):
    self.dev = serial.Serial(
      port=serial_device,
      baudrate=serial_rate,
      #timeout=self.config.timeout,
    )
    self.log("connected to", serial_device)

  def log(self, *msg):
    print " ".join(map(str, msg))

  def d7asp_fifo_flush(self, alp_command):
    data = self.parser.build_serial_frame(alp_command)
    self.dev.write(data)
    self.dev.flushOutput()
    self.log("Sending command of size", len(data))
    flush_done = False
    while not flush_done:
      data_received = self.dev.read()
      if len(data_received) > 0:
        (cmds, info) = self.parser.parse(data_received)

        for cmd in cmds:
          if cmd.flush_result != None:
            flush_done = True
            self.log("Flushing fifo {} done, success_bitmap={}"
                     .format(cmd.flush_result.operand.fifo_token, cmd.flush_result.operand.success_bitmap))

        for error in info["errors"]:
          error["buffer"] = " ".join(["0x{:02x}".format(ord(b)) for b in error["buffer"]])
          print error

  def read(self):
    data_received = self.dev.read_all()
    return self.parser.parse(data_received)