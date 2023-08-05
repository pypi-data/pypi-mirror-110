# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class OrderGift(object):
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
        'gift': 'bool',
        'gift_charge': 'Currency',
        'gift_charge_accounting_code': 'str',
        'gift_charge_refunded': 'Currency',
        'gift_email': 'str',
        'gift_message': 'str',
        'gift_wrap_accounting_code': 'str',
        'gift_wrap_cost': 'Currency',
        'gift_wrap_refunded': 'Currency',
        'gift_wrap_title': 'str'
    }

    attribute_map = {
        'gift': 'gift',
        'gift_charge': 'gift_charge',
        'gift_charge_accounting_code': 'gift_charge_accounting_code',
        'gift_charge_refunded': 'gift_charge_refunded',
        'gift_email': 'gift_email',
        'gift_message': 'gift_message',
        'gift_wrap_accounting_code': 'gift_wrap_accounting_code',
        'gift_wrap_cost': 'gift_wrap_cost',
        'gift_wrap_refunded': 'gift_wrap_refunded',
        'gift_wrap_title': 'gift_wrap_title'
    }

    def __init__(self, gift=None, gift_charge=None, gift_charge_accounting_code=None, gift_charge_refunded=None, gift_email=None, gift_message=None, gift_wrap_accounting_code=None, gift_wrap_cost=None, gift_wrap_refunded=None, gift_wrap_title=None):  # noqa: E501
        """OrderGift - a model defined in Swagger"""  # noqa: E501

        self._gift = None
        self._gift_charge = None
        self._gift_charge_accounting_code = None
        self._gift_charge_refunded = None
        self._gift_email = None
        self._gift_message = None
        self._gift_wrap_accounting_code = None
        self._gift_wrap_cost = None
        self._gift_wrap_refunded = None
        self._gift_wrap_title = None
        self.discriminator = None

        if gift is not None:
            self.gift = gift
        if gift_charge is not None:
            self.gift_charge = gift_charge
        if gift_charge_accounting_code is not None:
            self.gift_charge_accounting_code = gift_charge_accounting_code
        if gift_charge_refunded is not None:
            self.gift_charge_refunded = gift_charge_refunded
        if gift_email is not None:
            self.gift_email = gift_email
        if gift_message is not None:
            self.gift_message = gift_message
        if gift_wrap_accounting_code is not None:
            self.gift_wrap_accounting_code = gift_wrap_accounting_code
        if gift_wrap_cost is not None:
            self.gift_wrap_cost = gift_wrap_cost
        if gift_wrap_refunded is not None:
            self.gift_wrap_refunded = gift_wrap_refunded
        if gift_wrap_title is not None:
            self.gift_wrap_title = gift_wrap_title

    @property
    def gift(self):
        """Gets the gift of this OrderGift.  # noqa: E501

        True if the order is a gift  # noqa: E501

        :return: The gift of this OrderGift.  # noqa: E501
        :rtype: bool
        """
        return self._gift

    @gift.setter
    def gift(self, gift):
        """Sets the gift of this OrderGift.

        True if the order is a gift  # noqa: E501

        :param gift: The gift of this OrderGift.  # noqa: E501
        :type: bool
        """

        self._gift = gift

    @property
    def gift_charge(self):
        """Gets the gift_charge of this OrderGift.  # noqa: E501


        :return: The gift_charge of this OrderGift.  # noqa: E501
        :rtype: Currency
        """
        return self._gift_charge

    @gift_charge.setter
    def gift_charge(self, gift_charge):
        """Sets the gift_charge of this OrderGift.


        :param gift_charge: The gift_charge of this OrderGift.  # noqa: E501
        :type: Currency
        """

        self._gift_charge = gift_charge

    @property
    def gift_charge_accounting_code(self):
        """Gets the gift_charge_accounting_code of this OrderGift.  # noqa: E501

        QuickBooks code for the gift charge  # noqa: E501

        :return: The gift_charge_accounting_code of this OrderGift.  # noqa: E501
        :rtype: str
        """
        return self._gift_charge_accounting_code

    @gift_charge_accounting_code.setter
    def gift_charge_accounting_code(self, gift_charge_accounting_code):
        """Sets the gift_charge_accounting_code of this OrderGift.

        QuickBooks code for the gift charge  # noqa: E501

        :param gift_charge_accounting_code: The gift_charge_accounting_code of this OrderGift.  # noqa: E501
        :type: str
        """

        self._gift_charge_accounting_code = gift_charge_accounting_code

    @property
    def gift_charge_refunded(self):
        """Gets the gift_charge_refunded of this OrderGift.  # noqa: E501


        :return: The gift_charge_refunded of this OrderGift.  # noqa: E501
        :rtype: Currency
        """
        return self._gift_charge_refunded

    @gift_charge_refunded.setter
    def gift_charge_refunded(self, gift_charge_refunded):
        """Sets the gift_charge_refunded of this OrderGift.


        :param gift_charge_refunded: The gift_charge_refunded of this OrderGift.  # noqa: E501
        :type: Currency
        """

        self._gift_charge_refunded = gift_charge_refunded

    @property
    def gift_email(self):
        """Gets the gift_email of this OrderGift.  # noqa: E501

        Email address of the gift recipient  # noqa: E501

        :return: The gift_email of this OrderGift.  # noqa: E501
        :rtype: str
        """
        return self._gift_email

    @gift_email.setter
    def gift_email(self, gift_email):
        """Sets the gift_email of this OrderGift.

        Email address of the gift recipient  # noqa: E501

        :param gift_email: The gift_email of this OrderGift.  # noqa: E501
        :type: str
        """
        if gift_email is not None and len(gift_email) > 100:
            raise ValueError("Invalid value for `gift_email`, length must be less than or equal to `100`")  # noqa: E501

        self._gift_email = gift_email

    @property
    def gift_message(self):
        """Gets the gift_message of this OrderGift.  # noqa: E501

        Message to the gift recipient  # noqa: E501

        :return: The gift_message of this OrderGift.  # noqa: E501
        :rtype: str
        """
        return self._gift_message

    @gift_message.setter
    def gift_message(self, gift_message):
        """Sets the gift_message of this OrderGift.

        Message to the gift recipient  # noqa: E501

        :param gift_message: The gift_message of this OrderGift.  # noqa: E501
        :type: str
        """
        if gift_message is not None and len(gift_message) > 10000:
            raise ValueError("Invalid value for `gift_message`, length must be less than or equal to `10000`")  # noqa: E501

        self._gift_message = gift_message

    @property
    def gift_wrap_accounting_code(self):
        """Gets the gift_wrap_accounting_code of this OrderGift.  # noqa: E501

        QuickBooks code for the gift wrap charge  # noqa: E501

        :return: The gift_wrap_accounting_code of this OrderGift.  # noqa: E501
        :rtype: str
        """
        return self._gift_wrap_accounting_code

    @gift_wrap_accounting_code.setter
    def gift_wrap_accounting_code(self, gift_wrap_accounting_code):
        """Sets the gift_wrap_accounting_code of this OrderGift.

        QuickBooks code for the gift wrap charge  # noqa: E501

        :param gift_wrap_accounting_code: The gift_wrap_accounting_code of this OrderGift.  # noqa: E501
        :type: str
        """

        self._gift_wrap_accounting_code = gift_wrap_accounting_code

    @property
    def gift_wrap_cost(self):
        """Gets the gift_wrap_cost of this OrderGift.  # noqa: E501


        :return: The gift_wrap_cost of this OrderGift.  # noqa: E501
        :rtype: Currency
        """
        return self._gift_wrap_cost

    @gift_wrap_cost.setter
    def gift_wrap_cost(self, gift_wrap_cost):
        """Sets the gift_wrap_cost of this OrderGift.


        :param gift_wrap_cost: The gift_wrap_cost of this OrderGift.  # noqa: E501
        :type: Currency
        """

        self._gift_wrap_cost = gift_wrap_cost

    @property
    def gift_wrap_refunded(self):
        """Gets the gift_wrap_refunded of this OrderGift.  # noqa: E501


        :return: The gift_wrap_refunded of this OrderGift.  # noqa: E501
        :rtype: Currency
        """
        return self._gift_wrap_refunded

    @gift_wrap_refunded.setter
    def gift_wrap_refunded(self, gift_wrap_refunded):
        """Sets the gift_wrap_refunded of this OrderGift.


        :param gift_wrap_refunded: The gift_wrap_refunded of this OrderGift.  # noqa: E501
        :type: Currency
        """

        self._gift_wrap_refunded = gift_wrap_refunded

    @property
    def gift_wrap_title(self):
        """Gets the gift_wrap_title of this OrderGift.  # noqa: E501

        Title of the gift wrap that the customer wants used  # noqa: E501

        :return: The gift_wrap_title of this OrderGift.  # noqa: E501
        :rtype: str
        """
        return self._gift_wrap_title

    @gift_wrap_title.setter
    def gift_wrap_title(self, gift_wrap_title):
        """Sets the gift_wrap_title of this OrderGift.

        Title of the gift wrap that the customer wants used  # noqa: E501

        :param gift_wrap_title: The gift_wrap_title of this OrderGift.  # noqa: E501
        :type: str
        """
        if gift_wrap_title is not None and len(gift_wrap_title) > 30:
            raise ValueError("Invalid value for `gift_wrap_title`, length must be less than or equal to `30`")  # noqa: E501

        self._gift_wrap_title = gift_wrap_title

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
        if issubclass(OrderGift, dict):
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
        if not isinstance(other, OrderGift):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
