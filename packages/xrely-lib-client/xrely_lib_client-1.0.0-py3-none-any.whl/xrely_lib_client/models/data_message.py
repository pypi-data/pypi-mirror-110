# coding: utf-8

"""
    XRELY

    API Documentation for XRELY platform  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: contact@xrely.com
    
"""


import pprint
import re  # noqa: F401

import six


class DataMessage(object):
    """
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
        'committed': 'bool',
        'message': 'str'
    }

    attribute_map = {
        'committed': 'committed',
        'message': 'message'
    }

    def __init__(self, committed=None, message=None):  # noqa: E501
        """DataMessage - a model defined """  # noqa: E501

        self._committed = None
        self._message = None
        self.discriminator = None

        if committed is not None:
            self.committed = committed
        if message is not None:
            self.message = message

    @property
    def committed(self):
        """Gets the committed of this DataMessage.  # noqa: E501


        :return: The committed of this DataMessage.  # noqa: E501
        :rtype: bool
        """
        return self._committed

    @committed.setter
    def committed(self, committed):
        """Sets the committed of this DataMessage.


        :param committed: The committed of this DataMessage.  # noqa: E501
        :type: bool
        """

        self._committed = committed

    @property
    def message(self):
        """Gets the message of this DataMessage.  # noqa: E501


        :return: The message of this DataMessage.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this DataMessage.


        :param message: The message of this DataMessage.  # noqa: E501
        :type: str
        """

        self._message = message

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
        if issubclass(DataMessage, dict):
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
        if not isinstance(other, DataMessage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
