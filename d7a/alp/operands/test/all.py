# all.py
# author: Christophe VG <contact@christophe.vg>

# top-level aggregator for all unit tests for ALP modules

import unittest

from d7a.alp.operands.test.file import TestOffset, TestData

if __name__ == '__main__':
  tests = [ unittest.TestLoader().loadTestsFromTestCase(test)
            for test in [ 
                          TestOffset, TestData
                        ]
          ]

  all_tests = unittest.TestSuite( tests )
  unittest.TextTestRunner(verbosity=1).run(all_tests)
