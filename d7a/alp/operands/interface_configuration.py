from d7a.sp.configuration import Configuration
from d7a.support.schema import Validatable, Types


class InterfaceConfiguration(Validatable):

  SCHEMA = [{
    "interface_id"        : Types.BYTE(),
    "interface_configuration"    : Types.OBJECT(Configuration)
  }]

  def __init__(self, interface_id, interface_configuration):
    self.interface_id = interface_id
    self.interface_configuration   = interface_configuration
    super(InterfaceConfiguration, self).__init__()

  def __iter__(self):
    yield self.interface_id
    for byte in self.interface_configuration: yield byte

  def __str__(self):
    return "interface-id={}, status={}".format(self.interface_id, self.interface_configuration.__dict__)
