# ct.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for Compressed Time

import unittest

from d7a.types.ct import CT

class TestCT(unittest.TestCase):
  def test_default_constructor_is_zero(self):
    t = CT()
    self.assertEqual(int(t), 0)

  def test_ct_construction(self):
    for exp in [1, 7]:
      for mant in [1, 31]:
        try:
          t = CT(exp=exp, mant=mant)
        except ValueError:
          self.fail("CT constructor raised ExceptionType unexpectedly " +
                    "for exp={0}, mant={1}".format(exp, mant))

  def test_invalid_ct_constructions(self):
    def bad(args, kwargs): CT(**kwargs)
    self.assertRaises(ValueError, bad, [], { "exp"  : -1 })
    self.assertRaises(ValueError, bad, [], { "mant" : -1 })
    self.assertRaises(ValueError, bad, [], { "exp"  :  8 })
    self.assertRaises(ValueError, bad, [], { "mant" : 32 })

  def test_ct_conversion_to_int(self):
    self.assertEqual(int(CT(1,1)),   4)
    self.assertEqual(int(CT(2,2)),  32)
    self.assertEqual(int(CT(3,3)), 192)

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCT)
  unittest.TextTestRunner(verbosity=2).run(suite)
