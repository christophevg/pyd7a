#!/usr/bin/env python

# a simple chat client that displays alls received messages and offers an input
# line to send messages
# author: Christophe VG

import argparse
import serial

import curses
import curses.ascii

from d7a.serial_console_interface.parser import Parser
from pprint import pprint

from d7a.alp.command import Command
from d7a.alp.interface import InterfaceType
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.configuration import Configuration
from d7a.sp.qos import QoS
from d7a.system_files.uid import UidFile
from modem.modem import Modem

class ChatClient(object):
  def __init__(self):
    self.logs = []
    self.command = ""
    self.counter = 0

    argparser = argparse.ArgumentParser()

    argparser.add_argument("-s", "--serial", help="serial device /dev file", 
                           default="/dev/tty.usbserial-FTGCT0HY")
    argparser.add_argument("-b", "--baudrate", help="baudrate for serial device", 
                           type=int, default=115200)

    config = argparser.parse_args()
    self.modem = Modem(config.serial, config.baudrate, show_logging=False)

    self.setup_screen()
  
  def setup_screen(self):
    self.screen = curses.initscr()
    curses.noecho()       # no echo, we will render it
    curses.cbreak()       #
    curses.curs_set(0)    # hide cursor, we will fake it with inverted space
    curses.halfdelay(1)   # wait for 1/10 second when waiting for input
    self.screen.keypad(1)
    self.setup()

  def setup(self):
    (self.height, self.width) = self.screen.getmaxyx()
    self.setup_viewer_window()
    self.setup_prompt()
    
    self.refresh_logger_window()
    self.refresh_prompt()

  def setup_viewer_window(self):
    # create a pad, taking up the entire window, but the last two lines
    self.logger = curses.newpad(self.height-1, self.width)

  def setup_prompt(self):
    # create a window, taking up the entire window, but the last two lines
    self.prompt = curses.newpad(2, self.width)
    name = "ChatClient"
    self.prompt.addstr(0, 0, name + " " * (self.width-len(name)), curses.A_REVERSE)
    self.prompt.addstr(1, 0, "> ")
    self.update_command()
  
  def update_command(self):
    w = len(self.command)
    self.prompt.addstr(1, 2, self.command)
    self.prompt.addstr(1, 2 + w, " ", curses.A_REVERSE) # cursor
    self.prompt.addstr(1, 3 + w, " " * (self.width - 4 - w))
    self.refresh_prompt()
  
  def clean_up(self, msg=""):
    self.clean_up_screen()

  def clean_up_screen(self):
    curses.nocbreak();
    self.screen.keypad(0);
    curses.echo()
    curses.endwin()

  def add(self, text, style=curses.A_NORMAL):
    text = text.replace('\0', '')
    self.logs.append({ "text": text, "style": style})
    self.refresh_logger_window()

  def log(self, *msg):
    string = " ".join(map(str, msg))
    for line in string.splitlines():
      self.add(line)
    
  def refresh_logger_window(self):
    (height, width) = self.screen.getmaxyx()
    self.logger.erase()
    for y, line in enumerate(self.logs[-height+2:]):
      self.logger.addstr(y, 0, line["text"], line["style"])
    self.logger.refresh(0, 0, 0, 0, height-3, width)

  def refresh_prompt(self):
    (height, width) = self.screen.getmaxyx()
    self.prompt.refresh(0, 0, height-2, 0, height, width)

  def process(self):
    while True:
      # handle input from user
      self.handle_input()
      # Read from D7 modem and decode packets/commands
      (cmds, info) = self.modem.read()
      if len(info["errors"]) < 1:
        if len(cmds) > 0:
          origin = cmds[0].interface_status.operation.operand.interface_status.addressee.id
          data   = cmds[0].actions[0].operation.operand.data
          self.add(str(origin) + ": " + ''.join(map(str, data)))

  def handle_input(self):
    c = self.prompt.getch()
    if c == curses.ERR: return
    elif c == curses.KEY_RESIZE:
      self.setup()
    elif c == curses.ascii.DEL or c == curses.ascii.BS:
      self.command = self.command[:-1]
    elif c == ord('\n'):
      self.send()
      self.command = ""
    else:
      self.command += chr(c)
    self.update_command()

  def send(self):
    cmd = Command.create_with_return_file_data_action(
      file_id=0x40,
      data=map(ord, list(self.command)),
      interface_type=InterfaceType.D7ASP,
      interface_configuration=Configuration(
        qos=QoS(resp_mod=QoS.RESP_MODE_NO),
        addressee=Addressee(
          access_class=0,
          id_type=IdType.BCAST
        )
      )
    )
    self.modem.d7asp_fifo_flush(alp_command=cmd)
    self.add("me: " + self.command, curses.A_REVERSE)

if __name__ == "__main__":
  ChatClient().process()
