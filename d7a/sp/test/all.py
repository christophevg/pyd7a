# all.py
# author: Christophe VG <contact@christophe.vg>

# top-level aggregator for all unit tests for SP modules

import unittest

from d7a.sp.test.qos           import TestQoS
from d7a.sp.test.configuration import TestConfiguration

if __name__ == '__main__':
  tests = [ unittest.TestLoader().loadTestsFromTestCase(test)
            for test in [ 
                          TestQoS,
                          TestConfiguration
                         ]
          ]

  all_tests = unittest.TestSuite( tests )
  unittest.TextTestRunner(verbosity=1).run(all_tests)
