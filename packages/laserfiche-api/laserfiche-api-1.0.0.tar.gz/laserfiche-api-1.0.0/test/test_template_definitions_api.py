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
from laserfiche_api.api.template_definitions_api import TemplateDefinitionsApi  # noqa: E501
from laserfiche_api.rest import ApiException


class TestTemplateDefinitionsApi(unittest.TestCase):
    """TemplateDefinitionsApi unit test stubs"""

    def setUp(self):
        self.api = TemplateDefinitionsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_template_definition_by_id(self):
        """Test case for get_template_definition_by_id

        """
        pass

    def test_get_template_definitions(self):
        """Test case for get_template_definitions

        """
        pass

    def test_get_template_field_definitions(self):
        """Test case for get_template_field_definitions

        """
        pass


if __name__ == '__main__':
    unittest.main()
