# status.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7A SP Status information

import unittest

from d7a.types.ct     import CT
from d7a.d7anp.addressee import Addressee
from d7a.sp.session   import States
from d7a.sp.status    import Status

class TestStatus(unittest.TestCase):
  def test_byte_generation(self):
    expected = [
      0,                                              # channel_header
      16, 0,                                           # channel_id
      70,                                              # rxlevel (- dBm)
      80,                                              # link budget
      80,                                              # target rx level
      0,                                              # status
      100,                                              # fifo token
      0,                                              # seq
      20,                                              # response timeout
      16                                              # addressee ctrl (BCAST)
    ]
    bytes = bytearray(Status(
      channel_header=0, channel_index=16, rx_level=70, link_budget=80, target_rx_level=80,
      nls=False, missed=False, retry=False, unicast=False, fifo_token=100,
      seq_nr=0, response_to=CT(0, 20), addressee=Addressee()
    ))
    self.assertEqual(len(bytes), 11)
    for i in xrange(10):
      self.assertEqual(expected[i], bytes[i])

    bytes = bytearray(Status(
      channel_header=0, channel_index=16, rx_level=70, link_budget=80, target_rx_level=80,
      unicast=False, fifo_token=100, seq_nr=0, response_to=CT(0, 20), addressee=Addressee(),
      nls=True, missed=True, retry=True))

    expected[6] = int('11100000', 2) # nls, missed, retry, ucast
    self.assertEqual(len(bytes), 11)
    for i in xrange(10):
      self.assertEqual(expected[i], bytes[i])

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestStatus)
  unittest.TextTestRunner(verbosity=1).run(suite)
