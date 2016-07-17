#!/usr/bin/env python
import argparse
import time

from datetime import datetime

import binascii
import struct
import serial

from d7a.alp.operations.requests import ReadFileData
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.regular_action import RegularAction
from d7a.serial_console_interface.parser import Parser

from d7a.alp.command import Command
from d7a.system_files.dll_config import DllConfigFile
from d7a.system_files.uid import UidFile

from pyd7a.d7a.system_files.system_file_ids import SystemFileIds


class Modem:
  def __init__(self, serial_device, serial_rate):
    self.parser = Parser()
    self.setup_serial_device(serial_device, serial_rate)

  def setup_serial_device(self, serial_device, serial_rate):
    self.dev = serial.Serial(
      port=serial_device,
      baudrate=serial_rate,
      timeout=0.5,
    )

    self.uid = self.read_uid()
    print("connected to {}, node UID {}".format(serial_device, hex(self.uid)))

  def read_uid(self):
    self.send_command(Command.create_with_read_file_action_system_file(UidFile()))
    while True: # TODO timeout
      commands, info = self.read()
      for command in commands:
        for action in command.actions:
          if type(action) is RegularAction \
              and type(action.operation) is ReturnFileData \
              and action.operand.offset.id == SystemFileIds.UID:
            return struct.unpack(">Q", bytearray(action.operand.data))[0]


  def log(self, *msg):
    pass # print " ".join(map(str, msg))

  def send_command(self, alp_command):
    data = self.parser.build_serial_frame(alp_command)
    self.dev.write(data)
    self.dev.flushOutput()
    self.log("Sending command of size", len(data))

  def d7asp_fifo_flush(self, alp_command):
    self.send_command(alp_command)
    flush_done = False
    start_time = datetime.now()
    timeout = False
    while not flush_done and not timeout:
      data_received = self.dev.read()
      if len(data_received) > 0:
        (cmds, info) = self.parser.parse(data_received)

        for cmd in cmds:
          if cmd.flush_result != None:
            flush_done = True
            self.log("Flushing fifo {} done, success_bitmap={}"
                     .format(cmd.flush_result.operand.fifo_token, cmd.flush_result.operand.success_bitmap))
            break

        for error in info["errors"]:
          error["buffer"] = " ".join(["0x{:02x}".format(ord(b)) for b in error["buffer"]])
          print error

      if (datetime.now() - start_time).total_seconds() > 2:
        timeout = True
        self.log("Flush timed out, skipping")

  def read(self):
    # self.log("Bytes in serial buffer: {}".format(self.dev.inWaiting()))
    data_received = self.dev.read_all()
    return self.parser.parse(data_received)

  def cancel_read(self):
    self.stop_reading = True

  def read_async(self):
    self.stop_reading = False
    while not self.stop_reading:
      data_received = self.dev.read()
      if len(data_received) > 0:
        (cmds, info) = self.parser.parse(data_received)
        for error in info["errors"]:
          error["buffer"] = " ".join(["0x{:02x}".format(ord(b)) for b in error["buffer"]])
          print error

        for cmd in cmds:
          yield cmd
