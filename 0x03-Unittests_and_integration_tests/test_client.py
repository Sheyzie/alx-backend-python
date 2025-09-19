#!/usr/bin/env python3
"""
This module contains unit tests for client module functions including
class based GithubOrgClient org function to get resource from url
to get public repo url as well as if repo has license.

Each test case uses the unittest framework, and some tests use
mocking and parameterization to validate expected behavior.
"""


import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand(
        [
            ("google",),
            ("abc",)
        ]
    )
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json) -> None:
        """Test that GithubOrgClient.org returns correct data"""
        expected_result = {"org": org_name}
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once()
        self.assertEqual(result, expected_result)

    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns correct value from .org"""

        expected_url = "https://api.github.com/orgs/google/repos"
        payload = {"repos_url": expected_url}

        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            result = client._public_repos_url
            self.assertEqual(result, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names"""
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_repos_payload
        expected_url = "https://api.github.com/orgs/test-org/repos"

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = expected_url
            client = GithubOrgClient("test-org")
            result = client.public_repos()

            # Check that the result matches the repo names from the payload
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Assert that _public_repos_url was accessed once
            mock_url.assert_called_once()

            # Assert that get_json was called once with the expected URL
            mock_get_json.assert_called_once_with(expected_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean based on license match"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": fixtures.TEST_PAYLOAD[0][0],
        "repos_payload": fixtures.TEST_PAYLOAD[0][1],
        "expected_repos": fixtures.TEST_PAYLOAD[0][2],
        "apache2_repos": fixtures.TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for GithubOrgClient.public_repos with patched requests
    """

    @classmethod
    def setUpClass(cls):
        """Set up patching for requests.get and assign response based on URL"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Define URL responses mapping
        def side_effect(url):
            mock_resp = MagicMock()
            if url == "https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after all tests run"""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
