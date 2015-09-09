# all.py
# author: Christophe VG <contact@christophe.vg>

# top-level aggregator for all unit tests for types

import unittest

from d7a.types.test.ct import TestCT

if __name__ == '__main__':
  tests = [ unittest.TestLoader().loadTestsFromTestCase(test)
            for test in [ TestCT ]
          ]

  all_tests = unittest.TestSuite( tests )
  unittest.TextTestRunner(verbosity=1).run(all_tests)
