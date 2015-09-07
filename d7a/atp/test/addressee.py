# addressee.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ATP Addressee

import unittest

from d7a.atp.addressee import Addressee

class TestAddressee(unittest.TestCase):
  def test_unicast(self):
    addr = Addressee(ucast=False)
    self.assertFalse(addr.uses_unicast())
    addr.ucast = True
    self.assertTrue(addr.uses_unicast())

  def test_broadcast(self):
    addr = Addressee(ucast=False)
    self.assertTrue(addr.uses_broadcast())
    addr.ucast = True
    self.assertFalse(addr.uses_broadcast())

  def test_virtual_id(self):
    addr = Addressee(vid=False)
    self.assertFalse(addr.has_virtual_id())
    addr.vid = True
    self.assertTrue(addr.has_virtual_id())

  def test_id_type_is_broadcast(self):
    addr = Addressee(ucast=False, vid=False, id=None)
    self.assertEqual(addr.id_type, Addressee.BROADCAST)

  def test_id_type_is_virtual(self):
    addr = Addressee(ucast=True, vid=True, id=0x0)
    self.assertEqual(addr.id_type, Addressee.VIRTUAL)
    
  def test_id_type_is_universal(self):
    addr = Addressee(ucast=True, vid=False, id=0x0)
    self.assertEqual(addr.id_type, Addressee.UNIVERSAL)

  def test_id_length_of_broadcast_id(self):
    addr = Addressee(ucast=False, vid=False, id=None)
    self.assertEqual(addr.id_length, 0)

  def test_id_length_of_virtual_id(self):
    addr = Addressee(ucast=True, vid=True, id=0x0)
    self.assertEqual(addr.id_length, 2)

  def test_id_length_of_universal_id(self):
    addr = Addressee(ucast=True, vid=False, id=0x0)
    self.assertEqual(addr.id_length, 8)

  # negative tests
  # TODO

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAddressee)
  unittest.TextTestRunner(verbosity=2).run(suite)
