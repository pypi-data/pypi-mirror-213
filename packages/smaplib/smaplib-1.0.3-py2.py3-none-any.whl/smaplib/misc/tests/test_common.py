from __future__ import annotations

import unittest

import numpy as np
import pandas as pd

from .. import common as misc_common


class TestMiscCommon(unittest.TestCase):
    def test_cleanup_dict(self):
        test_dict = {
            "timestamp": pd.Timestamp("2023-01-01"),
            "none": None,
            "string": "test",
        }
        expected_dict = {
            "timestamp": "2023-01-01 00:00:00",
            "none": "<<NULL>>",
            "string": "test",
        }
        self.assertEqual(misc_common.cleanup_dict(test_dict), expected_dict)

    def test_format_value(self):
        self.assertEqual(misc_common.format_value(None), "<<NULL>>")
        self.assertEqual(
            misc_common.format_value(pd.Timestamp("2023-01-01")), "2023-01-01 00:00:00"
        )
        self.assertEqual(misc_common.format_value("test"), "test")

    def test_flatten_name_value_pairs(self):
        pairs = [("name", "John", "s"), ("age", 25, "d"), ("country", "USA", "s")]
        separator = ", "
        expected = "name: John, age: 25, country: USA"
        self.assertEqual(
            misc_common.flatten_name_value_pairs(pairs, separator), expected
        )

    def test_shift_array(self):
        ar = np.array([1, 2, 3, 4, 5])
        self.assertTrue(
            (
                misc_common.shift_array(ar, 2) == np.array([np.nan, np.nan, 1, 2, 3])
            ).all()
        )
        self.assertTrue(
            (
                misc_common.shift_array(ar, -2) == np.array([3, 4, 5, np.nan, np.nan])
            ).all()
        )

    def test_get_string_kind(self):
        self.assertEqual(
            misc_common.get_string_kind("http://example.com"),
            misc_common.StringKind.Url,
        )
        self.assertEqual(
            misc_common.get_string_kind("/home/user/test.txt"),
            misc_common.StringKind.Path,
        )
        self.assertEqual(
            misc_common.get_string_kind("this is a normal string"),
            misc_common.StringKind.Other,
        )
