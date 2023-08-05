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


class ItemShippingMethod(object):
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
        'cost': 'float',
        'each_additional_item_markup': 'float',
        'filter_to_if_available': 'bool',
        'first_item_markup': 'float',
        'fixed_shipping_cost': 'float',
        'flat_fee_markup': 'float',
        'free_shipping': 'bool',
        'per_item_fee_markup': 'float',
        'percentage_markup': 'float',
        'percentage_of_item_markup': 'float',
        'relax_restrictions_on_upsell': 'bool',
        'shipping_method': 'str',
        'shipping_method_oid': 'int',
        'shipping_method_validity': 'str',
        'signature_required': 'bool'
    }

    attribute_map = {
        'cost': 'cost',
        'each_additional_item_markup': 'each_additional_item_markup',
        'filter_to_if_available': 'filter_to_if_available',
        'first_item_markup': 'first_item_markup',
        'fixed_shipping_cost': 'fixed_shipping_cost',
        'flat_fee_markup': 'flat_fee_markup',
        'free_shipping': 'free_shipping',
        'per_item_fee_markup': 'per_item_fee_markup',
        'percentage_markup': 'percentage_markup',
        'percentage_of_item_markup': 'percentage_of_item_markup',
        'relax_restrictions_on_upsell': 'relax_restrictions_on_upsell',
        'shipping_method': 'shipping_method',
        'shipping_method_oid': 'shipping_method_oid',
        'shipping_method_validity': 'shipping_method_validity',
        'signature_required': 'signature_required'
    }

    def __init__(self, cost=None, each_additional_item_markup=None, filter_to_if_available=None, first_item_markup=None, fixed_shipping_cost=None, flat_fee_markup=None, free_shipping=None, per_item_fee_markup=None, percentage_markup=None, percentage_of_item_markup=None, relax_restrictions_on_upsell=None, shipping_method=None, shipping_method_oid=None, shipping_method_validity=None, signature_required=None):  # noqa: E501
        """ItemShippingMethod - a model defined in Swagger"""  # noqa: E501

        self._cost = None
        self._each_additional_item_markup = None
        self._filter_to_if_available = None
        self._first_item_markup = None
        self._fixed_shipping_cost = None
        self._flat_fee_markup = None
        self._free_shipping = None
        self._per_item_fee_markup = None
        self._percentage_markup = None
        self._percentage_of_item_markup = None
        self._relax_restrictions_on_upsell = None
        self._shipping_method = None
        self._shipping_method_oid = None
        self._shipping_method_validity = None
        self._signature_required = None
        self.discriminator = None

        if cost is not None:
            self.cost = cost
        if each_additional_item_markup is not None:
            self.each_additional_item_markup = each_additional_item_markup
        if filter_to_if_available is not None:
            self.filter_to_if_available = filter_to_if_available
        if first_item_markup is not None:
            self.first_item_markup = first_item_markup
        if fixed_shipping_cost is not None:
            self.fixed_shipping_cost = fixed_shipping_cost
        if flat_fee_markup is not None:
            self.flat_fee_markup = flat_fee_markup
        if free_shipping is not None:
            self.free_shipping = free_shipping
        if per_item_fee_markup is not None:
            self.per_item_fee_markup = per_item_fee_markup
        if percentage_markup is not None:
            self.percentage_markup = percentage_markup
        if percentage_of_item_markup is not None:
            self.percentage_of_item_markup = percentage_of_item_markup
        if relax_restrictions_on_upsell is not None:
            self.relax_restrictions_on_upsell = relax_restrictions_on_upsell
        if shipping_method is not None:
            self.shipping_method = shipping_method
        if shipping_method_oid is not None:
            self.shipping_method_oid = shipping_method_oid
        if shipping_method_validity is not None:
            self.shipping_method_validity = shipping_method_validity
        if signature_required is not None:
            self.signature_required = signature_required

    @property
    def cost(self):
        """Gets the cost of this ItemShippingMethod.  # noqa: E501

        Cost  # noqa: E501

        :return: The cost of this ItemShippingMethod.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this ItemShippingMethod.

        Cost  # noqa: E501

        :param cost: The cost of this ItemShippingMethod.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def each_additional_item_markup(self):
        """Gets the each_additional_item_markup of this ItemShippingMethod.  # noqa: E501

        Each additional item markup  # noqa: E501

        :return: The each_additional_item_markup of this ItemShippingMethod.  # noqa: E501
        :rtype: float
        """
        return self._each_additional_item_markup

    @each_additional_item_markup.setter
    def each_additional_item_markup(self, each_additional_item_markup):
        """Sets the each_additional_item_markup of this ItemShippingMethod.

        Each additional item markup  # noqa: E501

        :param each_additional_item_markup: The each_additional_item_markup of this ItemShippingMethod.  # noqa: E501
        :type: float
        """

        self._each_additional_item_markup = each_additional_item_markup

    @property
    def filter_to_if_available(self):
        """Gets the filter_to_if_available of this ItemShippingMethod.  # noqa: E501

        Filter to this method if available  # noqa: E501

        :return: The filter_to_if_available of this ItemShippingMethod.  # noqa: E501
        :rtype: bool
        """
        return self._filter_to_if_available

    @filter_to_if_available.setter
    def filter_to_if_available(self, filter_to_if_available):
        """Sets the filter_to_if_available of this ItemShippingMethod.

        Filter to this method if available  # noqa: E501

        :param filter_to_if_available: The filter_to_if_available of this ItemShippingMethod.  # noqa: E501
        :type: bool
        """

        self._filter_to_if_available = filter_to_if_available

    @property
    def first_item_markup(self):
        """Gets the first_item_markup of this ItemShippingMethod.  # noqa: E501

        First item markup  # noqa: E501

        :return: The first_item_markup of this ItemShippingMethod.  # noqa: E501
        :rtype: float
        """
        return self._first_item_markup

    @first_item_markup.setter
    def first_item_markup(self, first_item_markup):
        """Sets the first_item_markup of this ItemShippingMethod.

        First item markup  # noqa: E501

        :param first_item_markup: The first_item_markup of this ItemShippingMethod.  # noqa: E501
        :type: float
        """

        self._first_item_markup = first_item_markup

    @property
    def fixed_shipping_cost(self):
        """Gets the fixed_shipping_cost of this ItemShippingMethod.  # noqa: E501

        Fixed shipping cost  # noqa: E501

        :return: The fixed_shipping_cost of this ItemShippingMethod.  # noqa: E501
        :rtype: float
        """
        return self._fixed_shipping_cost

    @fixed_shipping_cost.setter
    def fixed_shipping_cost(self, fixed_shipping_cost):
        """Sets the fixed_shipping_cost of this ItemShippingMethod.

        Fixed shipping cost  # noqa: E501

        :param fixed_shipping_cost: The fixed_shipping_cost of this ItemShippingMethod.  # noqa: E501
        :type: float
        """

        self._fixed_shipping_cost = fixed_shipping_cost

    @property
    def flat_fee_markup(self):
        """Gets the flat_fee_markup of this ItemShippingMethod.  # noqa: E501

        Flat fee markup  # noqa: E501

        :return: The flat_fee_markup of this ItemShippingMethod.  # noqa: E501
        :rtype: float
        """
        return self._flat_fee_markup

    @flat_fee_markup.setter
    def flat_fee_markup(self, flat_fee_markup):
        """Sets the flat_fee_markup of this ItemShippingMethod.

        Flat fee markup  # noqa: E501

        :param flat_fee_markup: The flat_fee_markup of this ItemShippingMethod.  # noqa: E501
        :type: float
        """

        self._flat_fee_markup = flat_fee_markup

    @property
    def free_shipping(self):
        """Gets the free_shipping of this ItemShippingMethod.  # noqa: E501

        Free shipping  # noqa: E501

        :return: The free_shipping of this ItemShippingMethod.  # noqa: E501
        :rtype: bool
        """
        return self._free_shipping

    @free_shipping.setter
    def free_shipping(self, free_shipping):
        """Sets the free_shipping of this ItemShippingMethod.

        Free shipping  # noqa: E501

        :param free_shipping: The free_shipping of this ItemShippingMethod.  # noqa: E501
        :type: bool
        """

        self._free_shipping = free_shipping

    @property
    def per_item_fee_markup(self):
        """Gets the per_item_fee_markup of this ItemShippingMethod.  # noqa: E501

        Per item fee markup  # noqa: E501

        :return: The per_item_fee_markup of this ItemShippingMethod.  # noqa: E501
        :rtype: float
        """
        return self._per_item_fee_markup

    @per_item_fee_markup.setter
    def per_item_fee_markup(self, per_item_fee_markup):
        """Sets the per_item_fee_markup of this ItemShippingMethod.

        Per item fee markup  # noqa: E501

        :param per_item_fee_markup: The per_item_fee_markup of this ItemShippingMethod.  # noqa: E501
        :type: float
        """

        self._per_item_fee_markup = per_item_fee_markup

    @property
    def percentage_markup(self):
        """Gets the percentage_markup of this ItemShippingMethod.  # noqa: E501

        Percentage markup  # noqa: E501

        :return: The percentage_markup of this ItemShippingMethod.  # noqa: E501
        :rtype: float
        """
        return self._percentage_markup

    @percentage_markup.setter
    def percentage_markup(self, percentage_markup):
        """Sets the percentage_markup of this ItemShippingMethod.

        Percentage markup  # noqa: E501

        :param percentage_markup: The percentage_markup of this ItemShippingMethod.  # noqa: E501
        :type: float
        """

        self._percentage_markup = percentage_markup

    @property
    def percentage_of_item_markup(self):
        """Gets the percentage_of_item_markup of this ItemShippingMethod.  # noqa: E501

        Percentage of item markup  # noqa: E501

        :return: The percentage_of_item_markup of this ItemShippingMethod.  # noqa: E501
        :rtype: float
        """
        return self._percentage_of_item_markup

    @percentage_of_item_markup.setter
    def percentage_of_item_markup(self, percentage_of_item_markup):
        """Sets the percentage_of_item_markup of this ItemShippingMethod.

        Percentage of item markup  # noqa: E501

        :param percentage_of_item_markup: The percentage_of_item_markup of this ItemShippingMethod.  # noqa: E501
        :type: float
        """

        self._percentage_of_item_markup = percentage_of_item_markup

    @property
    def relax_restrictions_on_upsell(self):
        """Gets the relax_restrictions_on_upsell of this ItemShippingMethod.  # noqa: E501

        Relax restrictions on upsell  # noqa: E501

        :return: The relax_restrictions_on_upsell of this ItemShippingMethod.  # noqa: E501
        :rtype: bool
        """
        return self._relax_restrictions_on_upsell

    @relax_restrictions_on_upsell.setter
    def relax_restrictions_on_upsell(self, relax_restrictions_on_upsell):
        """Sets the relax_restrictions_on_upsell of this ItemShippingMethod.

        Relax restrictions on upsell  # noqa: E501

        :param relax_restrictions_on_upsell: The relax_restrictions_on_upsell of this ItemShippingMethod.  # noqa: E501
        :type: bool
        """

        self._relax_restrictions_on_upsell = relax_restrictions_on_upsell

    @property
    def shipping_method(self):
        """Gets the shipping_method of this ItemShippingMethod.  # noqa: E501

        Shipping method name  # noqa: E501

        :return: The shipping_method of this ItemShippingMethod.  # noqa: E501
        :rtype: str
        """
        return self._shipping_method

    @shipping_method.setter
    def shipping_method(self, shipping_method):
        """Sets the shipping_method of this ItemShippingMethod.

        Shipping method name  # noqa: E501

        :param shipping_method: The shipping_method of this ItemShippingMethod.  # noqa: E501
        :type: str
        """

        self._shipping_method = shipping_method

    @property
    def shipping_method_oid(self):
        """Gets the shipping_method_oid of this ItemShippingMethod.  # noqa: E501

        Shipping method object identifier  # noqa: E501

        :return: The shipping_method_oid of this ItemShippingMethod.  # noqa: E501
        :rtype: int
        """
        return self._shipping_method_oid

    @shipping_method_oid.setter
    def shipping_method_oid(self, shipping_method_oid):
        """Sets the shipping_method_oid of this ItemShippingMethod.

        Shipping method object identifier  # noqa: E501

        :param shipping_method_oid: The shipping_method_oid of this ItemShippingMethod.  # noqa: E501
        :type: int
        """

        self._shipping_method_oid = shipping_method_oid

    @property
    def shipping_method_validity(self):
        """Gets the shipping_method_validity of this ItemShippingMethod.  # noqa: E501

        Shipping method validity  # noqa: E501

        :return: The shipping_method_validity of this ItemShippingMethod.  # noqa: E501
        :rtype: str
        """
        return self._shipping_method_validity

    @shipping_method_validity.setter
    def shipping_method_validity(self, shipping_method_validity):
        """Sets the shipping_method_validity of this ItemShippingMethod.

        Shipping method validity  # noqa: E501

        :param shipping_method_validity: The shipping_method_validity of this ItemShippingMethod.  # noqa: E501
        :type: str
        """
        allowed_values = ["invalid for", "valid for", "valid only for"]  # noqa: E501
        if shipping_method_validity not in allowed_values:
            raise ValueError(
                "Invalid value for `shipping_method_validity` ({0}), must be one of {1}"  # noqa: E501
                .format(shipping_method_validity, allowed_values)
            )

        self._shipping_method_validity = shipping_method_validity

    @property
    def signature_required(self):
        """Gets the signature_required of this ItemShippingMethod.  # noqa: E501

        Signature required  # noqa: E501

        :return: The signature_required of this ItemShippingMethod.  # noqa: E501
        :rtype: bool
        """
        return self._signature_required

    @signature_required.setter
    def signature_required(self, signature_required):
        """Sets the signature_required of this ItemShippingMethod.

        Signature required  # noqa: E501

        :param signature_required: The signature_required of this ItemShippingMethod.  # noqa: E501
        :type: bool
        """

        self._signature_required = signature_required

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
        if issubclass(ItemShippingMethod, dict):
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
        if not isinstance(other, ItemShippingMethod):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
