import unittest
import os
import numpy as np
import sys

# Add .. to the PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

import lilfilter.filter_function as f


class TestFilterFunction(unittest.TestCase):
    def test1(self):
        for S in [6, 10]:
            # test symmetry
            self.assertTrue(f.get_function_at(S, -1) == f.get_function_at(S, 1))

            self.assertTrue(f.get_function_at(S, S) == 0)
            self.assertTrue(f.get_function_at(S, -S) == 0)
            self.assertTrue(f.get_function_at(S, -2.0*S) == 0)
            self.assertTrue(f.get_function_at(S, S - 0.01) != 0)
            self.assertTrue(f.get_function_at(S, -S+ 0.01) != 0)



if __name__ == "__main__":
    unittest.main()

