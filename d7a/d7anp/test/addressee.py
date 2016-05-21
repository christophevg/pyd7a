# addressee.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7 ATP Addressee

import unittest

from d7a.d7anp.addressee import Addressee, IdType


class TestAddressee(unittest.TestCase):
  def test_default_constructor(self):
    Addressee()
  
  def test_construction(self):
    Addressee(id_type=IdType.VID,  id=0xFFFF)
    Addressee(id_type=IdType.UID, id=0xFFFFFFFFFFFFFF)
  
  def test_id_length_of_broadcast_id(self):
    addr = Addressee(id_type=IdType.BCAST, id=None)
    self.assertEqual(addr.id_length, 0)

  def test_id_length_of_virtual_id(self):
    addr = Addressee(id_type=IdType.VID, id=0x0)
    self.assertEqual(addr.id_length, 2)

  def test_id_length_of_universal_id(self):
    addr = Addressee(id_type=IdType.UID, id=0x0)
    self.assertEqual(addr.id_length, 8)
  
  def test_id_type_propery(self):
    addr = Addressee()
    self.assertEqual(addr.id_type, IdType.BCAST)

  def test_access_class_property(self):
    addr = Addressee(access_class=0xF)
    self.assertEqual(addr.access_class, 0xF)

  def test_id_property(self):
    addr = Addressee(id_type=IdType.VID, id=0x1234)
    self.assertEqual(addr.id, 0x1234)

  # negative tests

  def test_addressee_id_is_positive_value(self):
    def bad(): addr = Addressee(id_type=IdType.BCAST, id=-1)
    self.assertRaises(ValueError, bad)
    def bad(): addr = Addressee(id_type=IdType.VID, id=-1)
    self.assertRaises(ValueError, bad)

  def test_virtual_addressee_id_consists_of_max_2_bytes(self):
    def bad(): addr = Addressee(id_type=IdType.VID,id=0x1FFFF)
    self.assertRaises(ValueError, bad)

  def test_universal_addressee_id_consists_of_max_8_bytes(self):
    def bad(): addr = Addressee(id_type=IdType.UID, id=0x1FFFFFFFFFFFFFFFF)
    self.assertRaises(ValueError, bad)

  def test_access_class_consists_of_max_4_bits(self):
    def bad(): addr = Addressee(access_class=0xFF)
    self.assertRaises(ValueError, bad)

  def test_invalid_id_type(self):
    def bad(): addr = Addressee(id_type=0)
    self.assertRaises(ValueError, bad)
    
  # byte generation
  
  def test_byte_generation(self):
    tests = [
      (Addressee(),                                           '00010000'),
      (Addressee(id_type=IdType.VID, id=0),                   '00110000'),
      (Addressee(id_type=IdType.UID, id=0),                   '00100000'),
      (Addressee(id_type=IdType.VID, id=0, access_class=15),  '00111111')
    ]
    for test in tests:
      addressee_ctrl = bytearray(test[0])[0]
      self.assertEqual(addressee_ctrl, int(test[1], 2))
    
    bs = bytearray(Addressee(id_type=IdType.VID, id=0x1234))
    self.assertEqual(len(bs), 3)
    self.assertEqual(bs[0], int('00110000', 2))
    self.assertEqual(bs[1], int('00010010', 2))
    self.assertEqual(bs[2], int('00110100', 2))

    bs = bytearray(Addressee(id_type=IdType.UID, id=0x1234567890123456))
    self.assertEqual(len(bs), 9)
    self.assertEqual(bs[0], int('00100000', 2))
    self.assertEqual(bs[1], int('00010010', 2))
    self.assertEqual(bs[2], int('00110100', 2))
    self.assertEqual(bs[3], int('01010110', 2))
    self.assertEqual(bs[4], int('01111000', 2))
    self.assertEqual(bs[5], int('10010000', 2))
    self.assertEqual(bs[6], int('00010010', 2))
    self.assertEqual(bs[7], int('00110100', 2))
    self.assertEqual(bs[8], int('01010110', 2))
    

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestAddressee)
  unittest.TextTestRunner(verbosity=2).run(suite)
