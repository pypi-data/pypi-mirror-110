# coding: utf-8

"""
    Intrinio API

    Welcome to the Intrinio API! Through our Financial Data Marketplace, we offer a wide selection of financial data feed APIs sourced by our own proprietary processes as well as from many data vendors. For a complete API request / response reference please view the [Intrinio API documentation](https://intrinio.com/documentation/api_v2). If you need additional help in using the API, please visit the [Intrinio website](https://intrinio.com) and click on the chat icon in the lower right corner.  # noqa: E501

    OpenAPI spec version: 2.23.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import intrinio_sdk
from intrinio_sdk.api.data_point_api import DataPointApi  # noqa: E501
from intrinio_sdk.rest import ApiException


class TestDataPointApi(unittest.TestCase):
    """DataPointApi unit test stubs"""

    def setUp(self):
        self.api = intrinio_sdk.api.data_point_api.DataPointApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_data_point_number(self):
        """Test case for get_data_point_number

        Data Point (Number)  # noqa: E501
        """
        pass

    def test_get_data_point_text(self):
        """Test case for get_data_point_text

        Data Point (Text)  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
