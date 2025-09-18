#!/usr/bin/env python3
"""
This module contains unit tests for client module functions including
class based GithubOrgClient org function to get resource from url
to get public repo url as well as if repo has license.

Each test case uses the unittest framework, and some tests use
mocking and parameterization to validate expected behavior.
"""


import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand(
        [
            ("google",),
            ("abc",)
        ]
    )
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data"""
        expected_result = {"org": org_name}
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once()
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
