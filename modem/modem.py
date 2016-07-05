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
  def __init__(self):
    self.parser = argparse.ArgumentParser(
      fromfile_prefix_chars = "@",
      description          = "Inferface with a D7 modem over a serial connection"
    )

    self.parser.add_argument("-s", "--serial", help="serial device /dev file", default="/dev/ttyUSB0")
    self.parser.add_argument("-r", "--rate", help="baudrate for serial device", type=int, default=115200)
    self.parser.add_argument("-t", "--timeout", help="connection read timeout", type=float, default=0.5)
    self.config = self.parser.parse_args()
    self.setup_serial_device()

  def setup_serial_device(self):
    self.dev = serial.Serial(
      port=self.config.serial,
      baudrate=self.config.rate,
      #timeout=self.config.timeout,
    )
    self.log("connected to", self.config.serial)

  def log(self, *msg):
    print " ".join(map(str, msg))

  def test(self, payload_size):
    command = Command.create_with_return_file_data_action(
      file_id=0x40,
      data=range(payload_size),
      interface_type=InterfaceType.D7ASP,
      interface_configuration=Configuration(
        qos=QoS(resp_mod=QoS.RESP_MODE_ALL),
        addressee=Addressee(
          access_class=2,
          id_type=IdType.BCAST
        )
      )
    )
    parser = Parser()
    data = parser.build_serial_frame(command)
    self.dev.write(data)
    self.dev.flushOutput()
    self.log("Sending command of size", len(data))
    flush_done = False
    while not flush_done:
      data_received = self.dev.read()
      if len(data_received) > 0:
        (cmds, info) = parser.parse(data_received)

        for cmd in cmds:
          if cmd.flush_result != None:
            flush_done = True
            self.log("Flushing fifo {} done, success_bitmap={}"
                     .format(cmd.flush_result.operand.fifo_token, cmd.flush_result.operand.success_bitmap))

        for error in info["errors"]:
          error["buffer"] = " ".join(["0x{:02x}".format(ord(b)) for b in error["buffer"]])
          print error

if __name__ == "__main__":
  start = time.time()
  modem = Modem()
  msg_count = 50
  payload_size = 100
  for i in range(msg_count):
    modem.test(payload_size)

  end = time.time()
  print("Sending {} messages completed in: {} s".format(msg_count, end - start))
  print("Throughput = {} bps with a payload size of {} bytes".format((msg_count * payload_size * 8) / (end - start), payload_size))