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


class OwnerSummary(object):
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
        'owner_cik': 'str',
        'owner_name': 'str'
    }

    attribute_map = {
        'owner_cik': 'owner_cik',
        'owner_name': 'owner_name'
    }

    def __init__(self, owner_cik=None, owner_name=None):  # noqa: E501
        """OwnerSummary - a model defined in Swagger"""  # noqa: E501

        self._owner_cik = None
        self._owner_name = None
        self.discriminator = None

        if owner_cik is not None:
            self.owner_cik = owner_cik
        if owner_name is not None:
            self.owner_name = owner_name

    @property
    def owner_cik(self):
        """Gets the owner_cik of this OwnerSummary.  # noqa: E501

        The Central Index Key issued by the SEC, which is the unique identifier all owner filings  # noqa: E501

        :return: The owner_cik of this OwnerSummary.  # noqa: E501
        :rtype: str
        """
        return self._owner_cik
        
    @property
    def owner_cik_dict(self):
        """Gets the owner_cik of this OwnerSummary.  # noqa: E501

        The Central Index Key issued by the SEC, which is the unique identifier all owner filings as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The owner_cik of this OwnerSummary.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.owner_cik
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
            result = { 'owner_cik': value }

        
        return result
        

    @owner_cik.setter
    def owner_cik(self, owner_cik):
        """Sets the owner_cik of this OwnerSummary.

        The Central Index Key issued by the SEC, which is the unique identifier all owner filings  # noqa: E501

        :param owner_cik: The owner_cik of this OwnerSummary.  # noqa: E501
        :type: str
        """

        self._owner_cik = owner_cik

    @property
    def owner_name(self):
        """Gets the owner_name of this OwnerSummary.  # noqa: E501

        The name of the owner  # noqa: E501

        :return: The owner_name of this OwnerSummary.  # noqa: E501
        :rtype: str
        """
        return self._owner_name
        
    @property
    def owner_name_dict(self):
        """Gets the owner_name of this OwnerSummary.  # noqa: E501

        The name of the owner as a dictionary. Useful for Panda Dataframes.  # noqa: E501

        :return: The owner_name of this OwnerSummary.  # noqa: E501
        :rtype: str
        """

        result = None

        value = self.owner_name
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
            result = { 'owner_name': value }

        
        return result
        

    @owner_name.setter
    def owner_name(self, owner_name):
        """Sets the owner_name of this OwnerSummary.

        The name of the owner  # noqa: E501

        :param owner_name: The owner_name of this OwnerSummary.  # noqa: E501
        :type: str
        """

        self._owner_name = owner_name

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
        if not isinstance(other, OwnerSummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
