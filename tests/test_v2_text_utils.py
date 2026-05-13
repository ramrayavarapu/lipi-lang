#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from lipi_v2.text_utils import find_assignment_index


class TestV2TextUtils(unittest.TestCase):
    def test_find_assignment_ignores_comparisons_inside_strings(self):
        line = 'value = "a == b"'
        self.assertEqual(find_assignment_index(line), 6)

    def test_find_assignment_ignores_escaped_quotes(self):
        line = 'value = "say \\"a == b\\""'
        self.assertEqual(find_assignment_index(line), 6)

    def test_find_assignment_skips_comparison_operators(self):
        self.assertEqual(find_assignment_index("x == 1"), -1)
        self.assertEqual(find_assignment_index("x != 1"), -1)
        self.assertEqual(find_assignment_index("x <= 1"), -1)
        self.assertEqual(find_assignment_index("x >= 1"), -1)


if __name__ == "__main__":
    unittest.main()
