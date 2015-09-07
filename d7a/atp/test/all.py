# all.py
# author: Christophe VG <contact@christophe.vg>

# top-level aggregator for all unit tests for ATP modules

import unittest

from d7a.atp.test.addressee import TestAddressee

if __name__ == '__main__':
  tests = [ unittest.TestLoader().loadTestsFromTestCase(test)
            for test in [ 
                          TestAddressee,
                         ]
          ]

  all_tests = unittest.TestSuite( tests )
  unittest.TextTestRunner(verbosity=2).run(all_tests)
