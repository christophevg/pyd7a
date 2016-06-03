
from d7a.d7anp.addressee import Addressee, IdType
from d7a.sp.qos import QoS
from d7a.alp.command import *
from d7a.serial_console_interface.parser import *
from pprint import pprint
import binascii

print("\n=== Return file data, with QoS, unicast ===\n")
cmd = Command.create_with_return_file_data_action(
  file_id=0x40,
  data=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  interface_type=InterfaceType.D7ASP,
  interface_configuration=Configuration(
    qos=QoS(resp_mod=QoS.RESP_MODE_ALL),
    addressee=Addressee(id_type=IdType.UID, id=1)
  )
)

serial_frame = Parser.build_serial_frame(cmd)

print("command:")
pprint(cmd.as_dict())
print("serial frame:")
pprint(binascii.hexlify(serial_frame).decode("ascii"))
pprint(serial_frame)