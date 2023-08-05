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


class EmailSegmentCustomersResponse(object):
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
        'customers': 'list[EmailSegmentCustomer]',
        'page_number': 'int',
        'page_size': 'int',
        'total_customers': 'int',
        'total_pages': 'int'
    }

    attribute_map = {
        'customers': 'customers',
        'page_number': 'page_number',
        'page_size': 'page_size',
        'total_customers': 'total_customers',
        'total_pages': 'total_pages'
    }

    def __init__(self, customers=None, page_number=None, page_size=None, total_customers=None, total_pages=None):  # noqa: E501
        """EmailSegmentCustomersResponse - a model defined in Swagger"""  # noqa: E501

        self._customers = None
        self._page_number = None
        self._page_size = None
        self._total_customers = None
        self._total_pages = None
        self.discriminator = None

        if customers is not None:
            self.customers = customers
        if page_number is not None:
            self.page_number = page_number
        if page_size is not None:
            self.page_size = page_size
        if total_customers is not None:
            self.total_customers = total_customers
        if total_pages is not None:
            self.total_pages = total_pages

    @property
    def customers(self):
        """Gets the customers of this EmailSegmentCustomersResponse.  # noqa: E501

        Customers on the page  # noqa: E501

        :return: The customers of this EmailSegmentCustomersResponse.  # noqa: E501
        :rtype: list[EmailSegmentCustomer]
        """
        return self._customers

    @customers.setter
    def customers(self, customers):
        """Sets the customers of this EmailSegmentCustomersResponse.

        Customers on the page  # noqa: E501

        :param customers: The customers of this EmailSegmentCustomersResponse.  # noqa: E501
        :type: list[EmailSegmentCustomer]
        """

        self._customers = customers

    @property
    def page_number(self):
        """Gets the page_number of this EmailSegmentCustomersResponse.  # noqa: E501

        Page number (one based offset)  # noqa: E501

        :return: The page_number of this EmailSegmentCustomersResponse.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this EmailSegmentCustomersResponse.

        Page number (one based offset)  # noqa: E501

        :param page_number: The page_number of this EmailSegmentCustomersResponse.  # noqa: E501
        :type: int
        """

        self._page_number = page_number

    @property
    def page_size(self):
        """Gets the page_size of this EmailSegmentCustomersResponse.  # noqa: E501

        Number of records per page  # noqa: E501

        :return: The page_size of this EmailSegmentCustomersResponse.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this EmailSegmentCustomersResponse.

        Number of records per page  # noqa: E501

        :param page_size: The page_size of this EmailSegmentCustomersResponse.  # noqa: E501
        :type: int
        """

        self._page_size = page_size

    @property
    def total_customers(self):
        """Gets the total_customers of this EmailSegmentCustomersResponse.  # noqa: E501

        Total customers  # noqa: E501

        :return: The total_customers of this EmailSegmentCustomersResponse.  # noqa: E501
        :rtype: int
        """
        return self._total_customers

    @total_customers.setter
    def total_customers(self, total_customers):
        """Sets the total_customers of this EmailSegmentCustomersResponse.

        Total customers  # noqa: E501

        :param total_customers: The total_customers of this EmailSegmentCustomersResponse.  # noqa: E501
        :type: int
        """

        self._total_customers = total_customers

    @property
    def total_pages(self):
        """Gets the total_pages of this EmailSegmentCustomersResponse.  # noqa: E501

        Total number of pages  # noqa: E501

        :return: The total_pages of this EmailSegmentCustomersResponse.  # noqa: E501
        :rtype: int
        """
        return self._total_pages

    @total_pages.setter
    def total_pages(self, total_pages):
        """Sets the total_pages of this EmailSegmentCustomersResponse.

        Total number of pages  # noqa: E501

        :param total_pages: The total_pages of this EmailSegmentCustomersResponse.  # noqa: E501
        :type: int
        """

        self._total_pages = total_pages

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
        if issubclass(EmailSegmentCustomersResponse, dict):
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
        if not isinstance(other, EmailSegmentCustomersResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
