# status.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7A SP Status information

import unittest

from d7a.types.ct     import CT
from d7a.d7anp.addressee import Addressee
from d7a.sp.session   import States
from d7a.sp.status    import Status

class TestStatus(unittest.TestCase):
  def test_default_constructor(self):
    c = Status()
  
  def test_configuration_switches_construction(self):
    Status(nls=True, missed=True, retry=True)
  
  def test_configuration_states_construction(self):
    for s in States.ALL: Status(state=s)
  
  def test_configuration_byte_constructions(self):
    Status(fifo_token=0x00) and Status(fifo_token=0xFF)
    Status(request_id=0x00) and Status(request_id=0xFF)

  def test_invalid_configuration_construction(self):
    def bad(args, kwargs): Status(**kwargs)
    self.assertRaises(ValueError, bad, [], { "fifo_token" : -1    })
    self.assertRaises(ValueError, bad, [], { "fifo_token" : 0x1FF })
    self.assertRaises(ValueError, bad, [], { "request_id" : -1    })
    self.assertRaises(ValueError, bad, [], { "request_id" : 0x1FF })
    self.assertRaises(ValueError, bad, [], { "state"      : -1    })
    self.assertRaises(ValueError, bad, [], { "state"      : 5     })
    self.assertRaises(ValueError, bad, [], { "addressee"  : None  })
    self.assertRaises(ValueError, bad, [], { "response_to": None  })
  
  def test_configuration_bad_composed_objects(self):
    def bad(args, kwargs): Status(**kwargs)
    self.assertRaises(ValueError, bad, [], { "response_to": Addressee() })
    self.assertRaises(ValueError, bad, [], { "addressee":   CT()        })
  
  def test_byte_generation(self):
    expected = [0 for x in xrange(11)]
    bytes = bytearray(Status())
    self.assertEqual(len(bytes), 11)
    for i in xrange(11):
      self.assertEqual(expected[i], bytes[i])

    bytes = bytearray(Status(nls=True, missed=True, retry=True))
    expected[6] = int('11100000', 2) # nls, missed, retry, state
    self.assertEqual(len(bytes), 11)
    for i in xrange(11):
      self.assertEqual(expected[i], bytes[i])

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestStatus)
  unittest.TextTestRunner(verbosity=1).run(suite)
