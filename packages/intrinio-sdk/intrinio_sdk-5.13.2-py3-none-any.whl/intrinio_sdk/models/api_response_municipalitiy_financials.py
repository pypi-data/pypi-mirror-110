# coding: utf-8

"""
    Intrinio API

    Welcome to the Intrinio API! Through our Financial Data Marketplace, we offer a wide selection of financial data feed APIs sourced by our own proprietary processes as well as from many data vendors. For a complete API request / response reference please view the [Intrinio API documentation](https://intrinio.com/documentation/api_v2). If you need additional help in using the API, please visit the [Intrinio website](https://intrinio.com) and click on the chat icon in the lower right corner.  # noqa: E501

    OpenAPI spec version: 2.23.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from intrinio_sdk.models.municipality import Municipality  # noqa: F401,E501
from intrinio_sdk.models.municipality_financial import MunicipalityFinancial  # noqa: F401,E501


class ApiResponseMunicipalitiyFinancials(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'financials': 'list[MunicipalityFinancial]',
        'municipality': 'Municipality'
    }

    attribute_map = {
        'financials': 'financials',
        'municipality': 'municipality'
    }

    def __init__(self, financials=None, municipality=None):  # noqa: E501
        """ApiResponseMunicipalitiyFinancials - a model defined in Swagger"""  # noqa: E501

        self._financials = None
        self._municipality = None
        self.discriminator = None

        if financials is not None:
            self.financials = financials
        if municipality is not None:
            self.municipality = municipality

    @property
    def financials(self):
        """Gets the financials of this ApiResponseMunicipalitiyFinancials.  # noqa: E501


        :return: The financials of this ApiResponseMunicipalitiyFinancials.  # noqa: E501
        :rtype: list[MunicipalityFinancial]
        """
        return self._financials
        
    @property
    def financials_dict(self):
        """Gets the financials of this ApiResponseMunicipalitiyFinancials.  # noqa: E501


        :return: The financials of this ApiResponseMunicipalitiyFinancials.  # noqa: E501
        :rtype: list[MunicipalityFinancial]
        """

        result = None

        value = self.financials
        if isinstance(value, list):
            result = list(map(
                lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                value
            ))
        elif hasattr(value, "to_dict"):
            result = value.to_dict()
        elif isinstance(value, dict):
            result = dict(map(
                lambda item: (item[0], item[1].to_dict())
                if hasattr(item[1], "to_dict") else item,
                value.items()
            ))
        else:
            result = { 'financials': value }

        
        return result
        

    @financials.setter
    def financials(self, financials):
        """Sets the financials of this ApiResponseMunicipalitiyFinancials.


        :param financials: The financials of this ApiResponseMunicipalitiyFinancials.  # noqa: E501
        :type: list[MunicipalityFinancial]
        """

        self._financials = financials

    @property
    def municipality(self):
        """Gets the municipality of this ApiResponseMunicipalitiyFinancials.  # noqa: E501


        :return: The municipality of this ApiResponseMunicipalitiyFinancials.  # noqa: E501
        :rtype: Municipality
        """
        return self._municipality
        
    @property
    def municipality_dict(self):
        """Gets the municipality of this ApiResponseMunicipalitiyFinancials.  # noqa: E501


        :return: The municipality of this ApiResponseMunicipalitiyFinancials.  # noqa: E501
        :rtype: Municipality
        """

        result = None

        value = self.municipality
        if isinstance(value, list):
            result = list(map(
                lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                value
            ))
        elif hasattr(value, "to_dict"):
            result = value.to_dict()
        elif isinstance(value, dict):
            result = dict(map(
                lambda item: (item[0], item[1].to_dict())
                if hasattr(item[1], "to_dict") else item,
                value.items()
            ))
        else:
            result = { 'municipality': value }

        
        return result
        

    @municipality.setter
    def municipality(self, municipality):
        """Sets the municipality of this ApiResponseMunicipalitiyFinancials.


        :param municipality: The municipality of this ApiResponseMunicipalitiyFinancials.  # noqa: E501
        :type: Municipality
        """

        self._municipality = municipality

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApiResponseMunicipalitiyFinancials):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
