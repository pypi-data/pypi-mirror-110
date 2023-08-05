# coding: utf-8

"""
    Laserfiche API

    Welcome to the Laserfiche API Swagger Playground. You can try out any of our API calls against your live Laserfiche Cloud account. Visit the developer center for more details: <a href=\"https://developer.laserfiche.com\">https://developer.laserfiche.com</a><p><strong>Build# : </strong>561590</p>  # noqa: E501

    OpenAPI spec version: 1-alpha
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import laserfiche_api
from laserfiche_api.api.access_tokens_api import AccessTokensApi  # noqa: E501
from laserfiche_api.rest import ApiException


class TestAccessTokensApi(unittest.TestCase):
    """AccessTokensApi unit test stubs"""

    def setUp(self):
        self.api = AccessTokensApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_access_token(self):
        """Test case for create_access_token

        """
        pass

    def test_invalidate_access_token(self):
        """Test case for invalidate_access_token

        """
        pass

    def test_refresh_access_token(self):
        """Test case for refresh_access_token

        """
        pass


if __name__ == '__main__':
    unittest.main()
