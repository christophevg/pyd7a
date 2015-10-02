# responses
# author: Christophe VG <contact@christophe.vg>

# class implementation of responses

from d7a.alp.operations.operation import Operation

from d7a.alp.command              import Command
from d7a.alp.action               import Action
from d7a.alp.payload              import Payload

from d7a.alp.operands.file        import Data, Offset

from d7a.sp.configuration         import Configuration
from d7a.sp.session               import States
from d7a.sp.qos                   import QoS

from d7a.tp.addressee             import Addressee

class ReturnFileData(Operation):
  def __init__(self, *args, **kwargs):
    self.op     = 32
    self.operand_class = Data
    super(ReturnFileData, self).__init__(*args, **kwargs)

  @staticmethod
  def send_command(addressee, file, data):
    return Command(
      interface=Configuration(
        state     = States.PENDING,
        qos       = QoS(resp_mod=QoS.ANY_CAST, ack_period=1, retry_single=3),
        addressee = Addressee(id=addressee)
      ),
      payload=Payload(
        actions=[
          Action(
            operation=ReturnFileData(
              operand=Data(
                data=data,
                offset=Offset(id=file)
              )
            )
          )
        ]
      )
    )
