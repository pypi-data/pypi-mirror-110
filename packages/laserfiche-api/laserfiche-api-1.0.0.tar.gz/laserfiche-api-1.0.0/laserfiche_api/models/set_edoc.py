# coding: utf-8

"""
    Laserfiche API

    Welcome to the Laserfiche API Swagger Playground. You can try out any of our API calls against your live Laserfiche Cloud account. Visit the developer center for more details: <a href=\"https://developer.laserfiche.com\">https://developer.laserfiche.com</a><p><strong>Build# : </strong>561590</p>  # noqa: E501

    OpenAPI spec version: 1-alpha
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class SetEdoc(object):
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
        'exceptions': 'list[APIServerException]'
    }

    attribute_map = {
        'exceptions': 'exceptions'
    }

    def __init__(self, exceptions=None):  # noqa: E501
        """SetEdoc - a model defined in Swagger"""  # noqa: E501
        self._exceptions = None
        self.discriminator = None
        if exceptions is not None:
            self.exceptions = exceptions

    @property
    def exceptions(self):
        """Gets the exceptions of this SetEdoc.  # noqa: E501

        The list of exceptions that occured when trying to perform the operation.  # noqa: E501

        :return: The exceptions of this SetEdoc.  # noqa: E501
        :rtype: list[APIServerException]
        """
        return self._exceptions

    @exceptions.setter
    def exceptions(self, exceptions):
        """Sets the exceptions of this SetEdoc.

        The list of exceptions that occured when trying to perform the operation.  # noqa: E501

        :param exceptions: The exceptions of this SetEdoc.  # noqa: E501
        :type: list[APIServerException]
        """

        self._exceptions = exceptions

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
        if issubclass(SetEdoc, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SetEdoc):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
