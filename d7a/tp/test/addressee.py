# addressee.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ATP Addressee

import unittest

from d7a.tp.addressee import Addressee

class TestAddressee(unittest.TestCase):
  def test_default_constructor(self):
    Addressee()
  
  def test_construction(self):
    Addressee(ucast=True, vid=True,  id=0xFFFF)
    Addressee(ucast=True, vid=False, id=0xFFFFFFFFFFFFFF)
  
  def test_invalid_construction(self):
    def bad(args, kwargs): Addressee(**kwargs)
    self.assertRaises(ValueError, bad, [], {"ucast":True, "vid":False})
    self.assertRaises(ValueError, bad, [], {"ucast":True, "vid":True})

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
  
  def test_ucast_propery(self):
    addr = Addressee(ucast=False)
    self.assertFalse(addr.ucast)

  def test_access_class_property(self):
    addr = Addressee(cl=0xF)
    self.assertEqual(addr.cl, 0xF)

  def test_id_property(self):
    addr = Addressee(ucast=True,vid=True,id=0x1234)
    self.assertEqual(addr.id, 0x1234)

  def test_manual_validation_of_unicast_without_id(self):
    addr = Addressee()
    addr.ucast = True
    def bad(): addr.validate()
    self.assertRaises(ValueError, bad)

  # negative tests

  def test_broadcasting_addressee_has_no_id(self):
    def bad(): addr = Addressee(ucast=False, id=0x123)
    self.assertRaises(ValueError, bad)

  def test_addressee_id_is_positive_value(self):
    def bad(): addr = Addressee(ucast=True,vid=True,id=-1)
    self.assertRaises(ValueError, bad)
    def bad(): addr = Addressee(ucast=True,vid=False,id=-1)
    self.assertRaises(ValueError, bad)

  def test_virtual_addressee_id_consists_of_max_2_bytes(self):
    def bad(): addr = Addressee(ucast=True,vid=True,id=0x1FFFF)
    self.assertRaises(ValueError, bad)

  def test_universal_addressee_id_consists_of_max_8_bytes(self):
    def bad(): addr = Addressee(ucast=True,vid=False,id=0x1FFFFFFFFFFFFFFFF)
    self.assertRaises(ValueError, bad)

  def test_access_class_consists_of_max_4_bits(self):
    def bad(): addr = Addressee(cl=0xFF)
    self.assertRaises(ValueError, bad)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAddressee)
  unittest.TextTestRunner(verbosity=2).run(suite)
