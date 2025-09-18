#!/usr/bin/env python3
"""
This module contains unit tests for utility functions including
accessing nested maps, fetching JSON data from URLs, and a
memoization decorator that caches method results.

Each test case uses the unittest framework, and some tests use
mocking and parameterization to validate expected behavior.
"""


import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the access_nested_map function in the utils module.
    These tests verify both successful value retrieval and expected
    exceptions when accessing keys in nested dictionaries.
    """

    @parameterized.expand(
        [
            ({"a": 1}, ('a',), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2)
        ]
    )
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence[str],
        expected: Any
    ) -> None:
        """
        Test access_nested_map returns the value for valid keys and paths.
        """

        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand(
        [
            ({}, ('a',), KeyError),
            ({"a": 1}, ("a", "b"), KeyError)
        ]
    )
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence[str],
        expected: Callable[[str], Exception]
    ) -> None:
        """
        Test that access_nested_map raises KeyError for invalid paths.
        """

        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Unit tests for the get_json function in the utils module.
    These tests verify that the function correctly fetches and returns
    JSON data from a given URL using the requests library.
    """

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns the expected JSON payload from a given URL.
        """

        with patch("requests.get") as mock_get_data:
            mock_get_data.return_value.json.return_value = test_payload
            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            mock_get_data.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Unit tests for the memoize decorator in the utils module.
    These tests verify that the decorated method is only executed once
    and its result is cached for subsequent accesses.
    """

    def test_memoize(self):
        """
        Test that a memoized method is only called once.
        """

        class TestClass:
            """
            A helper class with a memoized property for testing memoization.
            """

            def a_method(self):
                """
                Method that increments call_count and returns a fixed value.
                """

                self.call_count += 1
                return 42

            @memoize
            def a_property(self):
                """
                A memoized property that returns the result of a_method.
                """

                return self.a_method()

        test_obj = TestClass()
        with patch.object(test_obj, 'a_method', return_value=42) as mock_mtd:
            first = test_obj.a_property
            second = test_obj.a_property

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_mtd.assert_called_once()


if __name__ == "__main__":
    unittest.main()
