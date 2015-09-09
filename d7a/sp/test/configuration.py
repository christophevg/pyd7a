# configuration.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7A SP (FIFO) Configuration

import unittest

from d7a.types.ct         import CT
from d7a.tp.addressee     import Addressee
from d7a.sp.qos           import QoS
from d7a.sp.configuration import Configuration

class TestConfiguration(unittest.TestCase):
  def test_default_constructor(self):
    c = Configuration()
  
  def test_configuration_switches_construction(self):
    Configuration(nls=True, stop_on_err=True, preferred=True)
  
  def test_configuration_states_construction(self):
    for s in [ Configuration.IDLE, Configuration.DORMANT, Configuration.PENDING,
               Configuration.ACTIVE, Configuration.DONE ]:
      Configuration(state=s)
  
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

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestConfiguration)
  unittest.TextTestRunner(verbosity=1).run(suite)
