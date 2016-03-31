# command
# author: Christophe VG <contact@christophe.vg>

# class implementation of ALP commands

# a D7A ALP Command consists of 1 or more ALP Actions

from d7a.support.schema           import Validatable, Types
from d7a.alp.action              import Action

class Command(Validatable):
  
  SCHEMA = [{
    "actions": Types.LIST(Action)
  }]


  def __init__(self, actions=[]):
    self.actions = actions
    super(Command, self).__init__()

  def __iter__(self):
    for action in self.actions:
      for byte in action:
        yield byte
