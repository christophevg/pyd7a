# all.py
# author: Christophe VG <contact@christophe.vg>

# top-level aggregator for all unit tests for supporting modules

import unittest

if __name__ == '__main__':
  tests = [ unittest.TestLoader().loadTestsFromTestCase(test)
            for test in [ ]
          ]

  all_tests = unittest.TestSuite( tests )
  unittest.TextTestRunner(verbosity=2).run(all_tests)
