# configuration.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7A SP (FIFO) Configuration

import unittest

from d7a.types.ct         import CT
from d7a.sp.qos           import QoS
from d7a.sp.session       import States
from d7a.sp.configuration import Configuration

class TestConfiguration(unittest.TestCase):
  def test_default_constructor(self):
    c = Configuration()
  
  def test_configuration_switches_construction(self):
    Configuration(nls=True, stop_on_err=True, preferred=True)
  
  def test_configuration_states_construction(self):
    for s in States.ALL: Configuration(state=s)
  
  def test_configuration_start_construction(self):
    Configuration(start_id=0x00) and Configuration(start_id=0xFF)

  def test_invalid_configuration_construction(self):
    def bad(args, kwargs): Configuration(**kwargs)
    self.assertRaises(ValueError, bad, [], { "start_id"  : -1    })
    self.assertRaises(ValueError, bad, [], { "start_id"  : 0x1FF })
    self.assertRaises(ValueError, bad, [], { "state"     : -1    })
    self.assertRaises(ValueError, bad, [], { "state"     : 5     })
    self.assertRaises(ValueError, bad, [], { "qos"       : None  })
    self.assertRaises(ValueError, bad, [], { "addressee" : None  })
    self.assertRaises(ValueError, bad, [], { "dorm_to"   : None  })

  def test_configuration_bad_composed_objects(self):
    def bad(args, kwargs): Configuration(**kwargs)
    self.assertRaises(ValueError, bad, [], { "qos":       CT()  })
    self.assertRaises(ValueError, bad, [], { "dorm_to":   QoS() })
    self.assertRaises(ValueError, bad, [], { "addressee": QoS() })

  def test_byte_generation(self):
    # TODO: use mocking framework to mock sub-objects
    bytes = bytearray(Configuration())
    self.assertEqual(len(bytes), 8)
    self.assertEquals(bytes[0], int( '00000000', 2)) # fifo control
    self.assertEquals(bytes[1], int( '00000000', 2)) # qos
    self.assertEquals(bytes[2], int( '00000000', 2)) # qos
    self.assertEquals(bytes[3], int( '00000000', 2)) # qos
    self.assertEquals(bytes[4], int( '00000000', 2)) # qos
    self.assertEquals(bytes[5], int( '00000000', 2)) # dorm_to (CT)
    self.assertEquals(bytes[6], int( '00000000', 2)) # start_id
    self.assertEquals(bytes[7], int( '00000000', 2)) # addressee

    bytes = bytearray(Configuration(
      nls         = True,
      stop_on_err = True,
      preferred   = True,
      state       = States.PENDING,
      start_id    = 0x12
    ))
    self.assertEqual(len(bytes), 8)
    self.assertEquals(bytes[0], int( '10110010', 2)) # fifo control
    self.assertEquals(bytes[6], int( '00010010', 2)) # start_id

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestConfiguration)
  unittest.TextTestRunner(verbosity=1).run(suite)
