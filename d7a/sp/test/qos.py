# qos.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7A SP QoS Paramters 

import unittest

from d7a.sp.qos import QoS

class TestQoS(unittest.TestCase):
  def test_default_constructor(self):
    qos = QoS()

  def test_qos_ctrl_construction(self):
    for ack in [True, False]:
      for mod in [None, QoS.NO_CAST, QoS.ALL_CAST, QoS.ANY_CAST]:
        try:
          qos = QoS(ack_not_void=ack, resp_mod=mod)
        except ValueError:
          self.fail("QoS constructor raised ExceptionType unexpectedly " +
                    "for ack_not_void={0}, resp_mod={1}".format(ack, mod))

  def test_qos_invalid_ctrl_constructions(self):
    def bad(args, kwargs): QoS(**kwargs)
    self.assertRaises(ValueError, bad, [], { "ack_not_void": None })
    self.assertRaises(ValueError, bad, [], { "ack_not_void": 1    })
    self.assertRaises(ValueError, bad, [], { "resp_mod"    : -1   })
    self.assertRaises(ValueError, bad, [], { "resp_mod"    : 3    })

  def test_byte_boundaries_of_ack_period_and_retries(self):
    QoS(ack_period  = 0x00) and QoS(ack_period  = 0xFF)
    QoS(retry_single= 0x00) and QoS(retry_single= 0xFF)
    QoS(retry_total = 0x00) and QoS(retry_total = 0xFF)

  def test_byte_boundary_exceeding_for_ack_period_and_retries(self):
    def bad(args, kwargs): QoS(**kwargs)
    self.assertRaises(ValueError, bad, [], { "ack_period"  : -1    })
    self.assertRaises(ValueError, bad, [], { "ack_period"  : 0x1FF })
    self.assertRaises(ValueError, bad, [], { "retry_single": -1    })
    self.assertRaises(ValueError, bad, [], { "retry_single": 0x1FF })
    self.assertRaises(ValueError, bad, [], { "retry_total" : -1    })
    self.assertRaises(ValueError, bad, [], { "retry_total" : 0x1FF })
  
  def test_byte_generation(self):
    bytes = bytearray(QoS())
    self.assertEqual(len(bytes), 4)
    self.assertEqual(bytes[0], int('00000000', 2))
    self.assertEqual(bytes[1], int('00000000', 2))
    self.assertEqual(bytes[2], int('00000000', 2))
    self.assertEqual(bytes[3], int('00000000', 2))

    bytes = bytearray(QoS(
      ack_not_void= True,
      resp_mod    = QoS.ANY_CAST,
      ack_period  = 0x12,
      retry_single= 0x34,
      retry_total = 0x56
    ))
    self.assertEqual(len(bytes), 4)
    self.assertEqual(bytes[0], int('00010010', 2))
    self.assertEqual(bytes[1], int('00010010', 2))
    self.assertEqual(bytes[2], int('00110100', 2))
    self.assertEqual(bytes[3], int('01010110', 2))

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestQoS)
  unittest.TextTestRunner(verbosity=2).run(suite)
