# all.py
# author: Christophe VG <contact@christophe.vg>

# top-level aggregator for all unit tests for TP modules

import unittest

from d7a.tp.test.addressee import TestAddressee

if __name__ == '__main__':
  tests = [ unittest.TestLoader().loadTestsFromTestCase(test)
            for test in [ 
                          TestAddressee,
                         ]
          ]

  all_tests = unittest.TestSuite( tests )
  unittest.TextTestRunner(verbosity=1).run(all_tests)
