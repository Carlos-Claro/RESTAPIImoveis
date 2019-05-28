#!/usr/bin/python3.6

import unittest

class TestImoveis(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('a'.upper(),'A')


if __name__ == '__main__':
    unittest.main()
