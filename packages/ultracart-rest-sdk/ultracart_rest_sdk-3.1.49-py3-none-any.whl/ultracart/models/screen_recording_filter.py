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


class ScreenRecordingFilter(object):
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
        'affiliate_email': 'str',
        'affiliate_id': 'int',
        'communications_campaign_name': 'str',
        'communications_email_subject': 'str',
        'communications_flow_name': 'str',
        'email': 'ScreenRecordingFilterStringSearch',
        'email_domain': 'str',
        'email_identified': 'bool',
        'end_timestamp': 'ScreenRecordingFilterRangeDate',
        'esp_customer_uuid': 'str',
        'favorite': 'bool',
        'geolocation': 'ScreenRecordingFilterGeoDistance',
        'geolocation_country': 'ScreenRecordingFilterStringSearch',
        'geolocation_state': 'ScreenRecordingFilterStringSearch',
        'language_iso_code': 'ScreenRecordingFilterStringSearch',
        'last_x_days': 'int',
        'max_filter_values': 'int',
        'order_id': 'ScreenRecordingFilterStringSearch',
        'page_view_count': 'ScreenRecordingFilterRangeInteger',
        'page_views': 'list[ScreenRecordingFilterPageView]',
        'placed_order': 'bool',
        'preferred_language': 'ScreenRecordingFilterStringSearch',
        'referrer_domain': 'str',
        'screen_recording_uuids': 'list[str]',
        'screen_sizes': 'list[str]',
        'skip_filter_values': 'bool',
        'skip_hits': 'bool',
        'start_timestamp': 'ScreenRecordingFilterRangeDate',
        'tags': 'list[str]',
        'time_on_site': 'ScreenRecordingFilterRangeInteger',
        'user_agent_device_name': 'str',
        'user_agent_name': 'str',
        'user_agent_original': 'ScreenRecordingFilterStringSearch',
        'user_agent_os_name': 'str',
        'user_agent_os_version': 'str',
        'user_ip': 'ScreenRecordingFilterIpSearch',
        'utm_campaign': 'str',
        'utm_source': 'str',
        'visitor_number': 'int',
        'watched': 'bool'
    }

    attribute_map = {
        'affiliate_email': 'affiliate_email',
        'affiliate_id': 'affiliate_id',
        'communications_campaign_name': 'communications_campaign_name',
        'communications_email_subject': 'communications_email_subject',
        'communications_flow_name': 'communications_flow_name',
        'email': 'email',
        'email_domain': 'email_domain',
        'email_identified': 'email_identified',
        'end_timestamp': 'end_timestamp',
        'esp_customer_uuid': 'esp_customer_uuid',
        'favorite': 'favorite',
        'geolocation': 'geolocation',
        'geolocation_country': 'geolocation_country',
        'geolocation_state': 'geolocation_state',
        'language_iso_code': 'language_iso_code',
        'last_x_days': 'last_x_days',
        'max_filter_values': 'max_filter_values',
        'order_id': 'order_id',
        'page_view_count': 'page_view_count',
        'page_views': 'page_views',
        'placed_order': 'placed_order',
        'preferred_language': 'preferred_language',
        'referrer_domain': 'referrer_domain',
        'screen_recording_uuids': 'screen_recording_uuids',
        'screen_sizes': 'screen_sizes',
        'skip_filter_values': 'skip_filter_values',
        'skip_hits': 'skip_hits',
        'start_timestamp': 'start_timestamp',
        'tags': 'tags',
        'time_on_site': 'time_on_site',
        'user_agent_device_name': 'user_agent_device_name',
        'user_agent_name': 'user_agent_name',
        'user_agent_original': 'user_agent_original',
        'user_agent_os_name': 'user_agent_os_name',
        'user_agent_os_version': 'user_agent_os_version',
        'user_ip': 'user_ip',
        'utm_campaign': 'utm_campaign',
        'utm_source': 'utm_source',
        'visitor_number': 'visitor_number',
        'watched': 'watched'
    }

    def __init__(self, affiliate_email=None, affiliate_id=None, communications_campaign_name=None, communications_email_subject=None, communications_flow_name=None, email=None, email_domain=None, email_identified=None, end_timestamp=None, esp_customer_uuid=None, favorite=None, geolocation=None, geolocation_country=None, geolocation_state=None, language_iso_code=None, last_x_days=None, max_filter_values=None, order_id=None, page_view_count=None, page_views=None, placed_order=None, preferred_language=None, referrer_domain=None, screen_recording_uuids=None, screen_sizes=None, skip_filter_values=None, skip_hits=None, start_timestamp=None, tags=None, time_on_site=None, user_agent_device_name=None, user_agent_name=None, user_agent_original=None, user_agent_os_name=None, user_agent_os_version=None, user_ip=None, utm_campaign=None, utm_source=None, visitor_number=None, watched=None):  # noqa: E501
        """ScreenRecordingFilter - a model defined in Swagger"""  # noqa: E501

        self._affiliate_email = None
        self._affiliate_id = None
        self._communications_campaign_name = None
        self._communications_email_subject = None
        self._communications_flow_name = None
        self._email = None
        self._email_domain = None
        self._email_identified = None
        self._end_timestamp = None
        self._esp_customer_uuid = None
        self._favorite = None
        self._geolocation = None
        self._geolocation_country = None
        self._geolocation_state = None
        self._language_iso_code = None
        self._last_x_days = None
        self._max_filter_values = None
        self._order_id = None
        self._page_view_count = None
        self._page_views = None
        self._placed_order = None
        self._preferred_language = None
        self._referrer_domain = None
        self._screen_recording_uuids = None
        self._screen_sizes = None
        self._skip_filter_values = None
        self._skip_hits = None
        self._start_timestamp = None
        self._tags = None
        self._time_on_site = None
        self._user_agent_device_name = None
        self._user_agent_name = None
        self._user_agent_original = None
        self._user_agent_os_name = None
        self._user_agent_os_version = None
        self._user_ip = None
        self._utm_campaign = None
        self._utm_source = None
        self._visitor_number = None
        self._watched = None
        self.discriminator = None

        if affiliate_email is not None:
            self.affiliate_email = affiliate_email
        if affiliate_id is not None:
            self.affiliate_id = affiliate_id
        if communications_campaign_name is not None:
            self.communications_campaign_name = communications_campaign_name
        if communications_email_subject is not None:
            self.communications_email_subject = communications_email_subject
        if communications_flow_name is not None:
            self.communications_flow_name = communications_flow_name
        if email is not None:
            self.email = email
        if email_domain is not None:
            self.email_domain = email_domain
        if email_identified is not None:
            self.email_identified = email_identified
        if end_timestamp is not None:
            self.end_timestamp = end_timestamp
        if esp_customer_uuid is not None:
            self.esp_customer_uuid = esp_customer_uuid
        if favorite is not None:
            self.favorite = favorite
        if geolocation is not None:
            self.geolocation = geolocation
        if geolocation_country is not None:
            self.geolocation_country = geolocation_country
        if geolocation_state is not None:
            self.geolocation_state = geolocation_state
        if language_iso_code is not None:
            self.language_iso_code = language_iso_code
        if last_x_days is not None:
            self.last_x_days = last_x_days
        if max_filter_values is not None:
            self.max_filter_values = max_filter_values
        if order_id is not None:
            self.order_id = order_id
        if page_view_count is not None:
            self.page_view_count = page_view_count
        if page_views is not None:
            self.page_views = page_views
        if placed_order is not None:
            self.placed_order = placed_order
        if preferred_language is not None:
            self.preferred_language = preferred_language
        if referrer_domain is not None:
            self.referrer_domain = referrer_domain
        if screen_recording_uuids is not None:
            self.screen_recording_uuids = screen_recording_uuids
        if screen_sizes is not None:
            self.screen_sizes = screen_sizes
        if skip_filter_values is not None:
            self.skip_filter_values = skip_filter_values
        if skip_hits is not None:
            self.skip_hits = skip_hits
        if start_timestamp is not None:
            self.start_timestamp = start_timestamp
        if tags is not None:
            self.tags = tags
        if time_on_site is not None:
            self.time_on_site = time_on_site
        if user_agent_device_name is not None:
            self.user_agent_device_name = user_agent_device_name
        if user_agent_name is not None:
            self.user_agent_name = user_agent_name
        if user_agent_original is not None:
            self.user_agent_original = user_agent_original
        if user_agent_os_name is not None:
            self.user_agent_os_name = user_agent_os_name
        if user_agent_os_version is not None:
            self.user_agent_os_version = user_agent_os_version
        if user_ip is not None:
            self.user_ip = user_ip
        if utm_campaign is not None:
            self.utm_campaign = utm_campaign
        if utm_source is not None:
            self.utm_source = utm_source
        if visitor_number is not None:
            self.visitor_number = visitor_number
        if watched is not None:
            self.watched = watched

    @property
    def affiliate_email(self):
        """Gets the affiliate_email of this ScreenRecordingFilter.  # noqa: E501


        :return: The affiliate_email of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._affiliate_email

    @affiliate_email.setter
    def affiliate_email(self, affiliate_email):
        """Sets the affiliate_email of this ScreenRecordingFilter.


        :param affiliate_email: The affiliate_email of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._affiliate_email = affiliate_email

    @property
    def affiliate_id(self):
        """Gets the affiliate_id of this ScreenRecordingFilter.  # noqa: E501


        :return: The affiliate_id of this ScreenRecordingFilter.  # noqa: E501
        :rtype: int
        """
        return self._affiliate_id

    @affiliate_id.setter
    def affiliate_id(self, affiliate_id):
        """Sets the affiliate_id of this ScreenRecordingFilter.


        :param affiliate_id: The affiliate_id of this ScreenRecordingFilter.  # noqa: E501
        :type: int
        """

        self._affiliate_id = affiliate_id

    @property
    def communications_campaign_name(self):
        """Gets the communications_campaign_name of this ScreenRecordingFilter.  # noqa: E501


        :return: The communications_campaign_name of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._communications_campaign_name

    @communications_campaign_name.setter
    def communications_campaign_name(self, communications_campaign_name):
        """Sets the communications_campaign_name of this ScreenRecordingFilter.


        :param communications_campaign_name: The communications_campaign_name of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._communications_campaign_name = communications_campaign_name

    @property
    def communications_email_subject(self):
        """Gets the communications_email_subject of this ScreenRecordingFilter.  # noqa: E501


        :return: The communications_email_subject of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._communications_email_subject

    @communications_email_subject.setter
    def communications_email_subject(self, communications_email_subject):
        """Sets the communications_email_subject of this ScreenRecordingFilter.


        :param communications_email_subject: The communications_email_subject of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._communications_email_subject = communications_email_subject

    @property
    def communications_flow_name(self):
        """Gets the communications_flow_name of this ScreenRecordingFilter.  # noqa: E501


        :return: The communications_flow_name of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._communications_flow_name

    @communications_flow_name.setter
    def communications_flow_name(self, communications_flow_name):
        """Sets the communications_flow_name of this ScreenRecordingFilter.


        :param communications_flow_name: The communications_flow_name of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._communications_flow_name = communications_flow_name

    @property
    def email(self):
        """Gets the email of this ScreenRecordingFilter.  # noqa: E501


        :return: The email of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterStringSearch
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this ScreenRecordingFilter.


        :param email: The email of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterStringSearch
        """

        self._email = email

    @property
    def email_domain(self):
        """Gets the email_domain of this ScreenRecordingFilter.  # noqa: E501


        :return: The email_domain of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._email_domain

    @email_domain.setter
    def email_domain(self, email_domain):
        """Sets the email_domain of this ScreenRecordingFilter.


        :param email_domain: The email_domain of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._email_domain = email_domain

    @property
    def email_identified(self):
        """Gets the email_identified of this ScreenRecordingFilter.  # noqa: E501


        :return: The email_identified of this ScreenRecordingFilter.  # noqa: E501
        :rtype: bool
        """
        return self._email_identified

    @email_identified.setter
    def email_identified(self, email_identified):
        """Sets the email_identified of this ScreenRecordingFilter.


        :param email_identified: The email_identified of this ScreenRecordingFilter.  # noqa: E501
        :type: bool
        """

        self._email_identified = email_identified

    @property
    def end_timestamp(self):
        """Gets the end_timestamp of this ScreenRecordingFilter.  # noqa: E501


        :return: The end_timestamp of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterRangeDate
        """
        return self._end_timestamp

    @end_timestamp.setter
    def end_timestamp(self, end_timestamp):
        """Sets the end_timestamp of this ScreenRecordingFilter.


        :param end_timestamp: The end_timestamp of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterRangeDate
        """

        self._end_timestamp = end_timestamp

    @property
    def esp_customer_uuid(self):
        """Gets the esp_customer_uuid of this ScreenRecordingFilter.  # noqa: E501


        :return: The esp_customer_uuid of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._esp_customer_uuid

    @esp_customer_uuid.setter
    def esp_customer_uuid(self, esp_customer_uuid):
        """Sets the esp_customer_uuid of this ScreenRecordingFilter.


        :param esp_customer_uuid: The esp_customer_uuid of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._esp_customer_uuid = esp_customer_uuid

    @property
    def favorite(self):
        """Gets the favorite of this ScreenRecordingFilter.  # noqa: E501


        :return: The favorite of this ScreenRecordingFilter.  # noqa: E501
        :rtype: bool
        """
        return self._favorite

    @favorite.setter
    def favorite(self, favorite):
        """Sets the favorite of this ScreenRecordingFilter.


        :param favorite: The favorite of this ScreenRecordingFilter.  # noqa: E501
        :type: bool
        """

        self._favorite = favorite

    @property
    def geolocation(self):
        """Gets the geolocation of this ScreenRecordingFilter.  # noqa: E501


        :return: The geolocation of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterGeoDistance
        """
        return self._geolocation

    @geolocation.setter
    def geolocation(self, geolocation):
        """Sets the geolocation of this ScreenRecordingFilter.


        :param geolocation: The geolocation of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterGeoDistance
        """

        self._geolocation = geolocation

    @property
    def geolocation_country(self):
        """Gets the geolocation_country of this ScreenRecordingFilter.  # noqa: E501


        :return: The geolocation_country of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterStringSearch
        """
        return self._geolocation_country

    @geolocation_country.setter
    def geolocation_country(self, geolocation_country):
        """Sets the geolocation_country of this ScreenRecordingFilter.


        :param geolocation_country: The geolocation_country of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterStringSearch
        """

        self._geolocation_country = geolocation_country

    @property
    def geolocation_state(self):
        """Gets the geolocation_state of this ScreenRecordingFilter.  # noqa: E501


        :return: The geolocation_state of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterStringSearch
        """
        return self._geolocation_state

    @geolocation_state.setter
    def geolocation_state(self, geolocation_state):
        """Sets the geolocation_state of this ScreenRecordingFilter.


        :param geolocation_state: The geolocation_state of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterStringSearch
        """

        self._geolocation_state = geolocation_state

    @property
    def language_iso_code(self):
        """Gets the language_iso_code of this ScreenRecordingFilter.  # noqa: E501


        :return: The language_iso_code of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterStringSearch
        """
        return self._language_iso_code

    @language_iso_code.setter
    def language_iso_code(self, language_iso_code):
        """Sets the language_iso_code of this ScreenRecordingFilter.


        :param language_iso_code: The language_iso_code of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterStringSearch
        """

        self._language_iso_code = language_iso_code

    @property
    def last_x_days(self):
        """Gets the last_x_days of this ScreenRecordingFilter.  # noqa: E501


        :return: The last_x_days of this ScreenRecordingFilter.  # noqa: E501
        :rtype: int
        """
        return self._last_x_days

    @last_x_days.setter
    def last_x_days(self, last_x_days):
        """Sets the last_x_days of this ScreenRecordingFilter.


        :param last_x_days: The last_x_days of this ScreenRecordingFilter.  # noqa: E501
        :type: int
        """

        self._last_x_days = last_x_days

    @property
    def max_filter_values(self):
        """Gets the max_filter_values of this ScreenRecordingFilter.  # noqa: E501


        :return: The max_filter_values of this ScreenRecordingFilter.  # noqa: E501
        :rtype: int
        """
        return self._max_filter_values

    @max_filter_values.setter
    def max_filter_values(self, max_filter_values):
        """Sets the max_filter_values of this ScreenRecordingFilter.


        :param max_filter_values: The max_filter_values of this ScreenRecordingFilter.  # noqa: E501
        :type: int
        """

        self._max_filter_values = max_filter_values

    @property
    def order_id(self):
        """Gets the order_id of this ScreenRecordingFilter.  # noqa: E501


        :return: The order_id of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterStringSearch
        """
        return self._order_id

    @order_id.setter
    def order_id(self, order_id):
        """Sets the order_id of this ScreenRecordingFilter.


        :param order_id: The order_id of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterStringSearch
        """

        self._order_id = order_id

    @property
    def page_view_count(self):
        """Gets the page_view_count of this ScreenRecordingFilter.  # noqa: E501


        :return: The page_view_count of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterRangeInteger
        """
        return self._page_view_count

    @page_view_count.setter
    def page_view_count(self, page_view_count):
        """Sets the page_view_count of this ScreenRecordingFilter.


        :param page_view_count: The page_view_count of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterRangeInteger
        """

        self._page_view_count = page_view_count

    @property
    def page_views(self):
        """Gets the page_views of this ScreenRecordingFilter.  # noqa: E501


        :return: The page_views of this ScreenRecordingFilter.  # noqa: E501
        :rtype: list[ScreenRecordingFilterPageView]
        """
        return self._page_views

    @page_views.setter
    def page_views(self, page_views):
        """Sets the page_views of this ScreenRecordingFilter.


        :param page_views: The page_views of this ScreenRecordingFilter.  # noqa: E501
        :type: list[ScreenRecordingFilterPageView]
        """

        self._page_views = page_views

    @property
    def placed_order(self):
        """Gets the placed_order of this ScreenRecordingFilter.  # noqa: E501


        :return: The placed_order of this ScreenRecordingFilter.  # noqa: E501
        :rtype: bool
        """
        return self._placed_order

    @placed_order.setter
    def placed_order(self, placed_order):
        """Sets the placed_order of this ScreenRecordingFilter.


        :param placed_order: The placed_order of this ScreenRecordingFilter.  # noqa: E501
        :type: bool
        """

        self._placed_order = placed_order

    @property
    def preferred_language(self):
        """Gets the preferred_language of this ScreenRecordingFilter.  # noqa: E501


        :return: The preferred_language of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterStringSearch
        """
        return self._preferred_language

    @preferred_language.setter
    def preferred_language(self, preferred_language):
        """Sets the preferred_language of this ScreenRecordingFilter.


        :param preferred_language: The preferred_language of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterStringSearch
        """

        self._preferred_language = preferred_language

    @property
    def referrer_domain(self):
        """Gets the referrer_domain of this ScreenRecordingFilter.  # noqa: E501


        :return: The referrer_domain of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._referrer_domain

    @referrer_domain.setter
    def referrer_domain(self, referrer_domain):
        """Sets the referrer_domain of this ScreenRecordingFilter.


        :param referrer_domain: The referrer_domain of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._referrer_domain = referrer_domain

    @property
    def screen_recording_uuids(self):
        """Gets the screen_recording_uuids of this ScreenRecordingFilter.  # noqa: E501


        :return: The screen_recording_uuids of this ScreenRecordingFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._screen_recording_uuids

    @screen_recording_uuids.setter
    def screen_recording_uuids(self, screen_recording_uuids):
        """Sets the screen_recording_uuids of this ScreenRecordingFilter.


        :param screen_recording_uuids: The screen_recording_uuids of this ScreenRecordingFilter.  # noqa: E501
        :type: list[str]
        """

        self._screen_recording_uuids = screen_recording_uuids

    @property
    def screen_sizes(self):
        """Gets the screen_sizes of this ScreenRecordingFilter.  # noqa: E501


        :return: The screen_sizes of this ScreenRecordingFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._screen_sizes

    @screen_sizes.setter
    def screen_sizes(self, screen_sizes):
        """Sets the screen_sizes of this ScreenRecordingFilter.


        :param screen_sizes: The screen_sizes of this ScreenRecordingFilter.  # noqa: E501
        :type: list[str]
        """

        self._screen_sizes = screen_sizes

    @property
    def skip_filter_values(self):
        """Gets the skip_filter_values of this ScreenRecordingFilter.  # noqa: E501


        :return: The skip_filter_values of this ScreenRecordingFilter.  # noqa: E501
        :rtype: bool
        """
        return self._skip_filter_values

    @skip_filter_values.setter
    def skip_filter_values(self, skip_filter_values):
        """Sets the skip_filter_values of this ScreenRecordingFilter.


        :param skip_filter_values: The skip_filter_values of this ScreenRecordingFilter.  # noqa: E501
        :type: bool
        """

        self._skip_filter_values = skip_filter_values

    @property
    def skip_hits(self):
        """Gets the skip_hits of this ScreenRecordingFilter.  # noqa: E501


        :return: The skip_hits of this ScreenRecordingFilter.  # noqa: E501
        :rtype: bool
        """
        return self._skip_hits

    @skip_hits.setter
    def skip_hits(self, skip_hits):
        """Sets the skip_hits of this ScreenRecordingFilter.


        :param skip_hits: The skip_hits of this ScreenRecordingFilter.  # noqa: E501
        :type: bool
        """

        self._skip_hits = skip_hits

    @property
    def start_timestamp(self):
        """Gets the start_timestamp of this ScreenRecordingFilter.  # noqa: E501


        :return: The start_timestamp of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterRangeDate
        """
        return self._start_timestamp

    @start_timestamp.setter
    def start_timestamp(self, start_timestamp):
        """Sets the start_timestamp of this ScreenRecordingFilter.


        :param start_timestamp: The start_timestamp of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterRangeDate
        """

        self._start_timestamp = start_timestamp

    @property
    def tags(self):
        """Gets the tags of this ScreenRecordingFilter.  # noqa: E501


        :return: The tags of this ScreenRecordingFilter.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ScreenRecordingFilter.


        :param tags: The tags of this ScreenRecordingFilter.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def time_on_site(self):
        """Gets the time_on_site of this ScreenRecordingFilter.  # noqa: E501


        :return: The time_on_site of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterRangeInteger
        """
        return self._time_on_site

    @time_on_site.setter
    def time_on_site(self, time_on_site):
        """Sets the time_on_site of this ScreenRecordingFilter.


        :param time_on_site: The time_on_site of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterRangeInteger
        """

        self._time_on_site = time_on_site

    @property
    def user_agent_device_name(self):
        """Gets the user_agent_device_name of this ScreenRecordingFilter.  # noqa: E501


        :return: The user_agent_device_name of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._user_agent_device_name

    @user_agent_device_name.setter
    def user_agent_device_name(self, user_agent_device_name):
        """Sets the user_agent_device_name of this ScreenRecordingFilter.


        :param user_agent_device_name: The user_agent_device_name of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._user_agent_device_name = user_agent_device_name

    @property
    def user_agent_name(self):
        """Gets the user_agent_name of this ScreenRecordingFilter.  # noqa: E501


        :return: The user_agent_name of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._user_agent_name

    @user_agent_name.setter
    def user_agent_name(self, user_agent_name):
        """Sets the user_agent_name of this ScreenRecordingFilter.


        :param user_agent_name: The user_agent_name of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._user_agent_name = user_agent_name

    @property
    def user_agent_original(self):
        """Gets the user_agent_original of this ScreenRecordingFilter.  # noqa: E501


        :return: The user_agent_original of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterStringSearch
        """
        return self._user_agent_original

    @user_agent_original.setter
    def user_agent_original(self, user_agent_original):
        """Sets the user_agent_original of this ScreenRecordingFilter.


        :param user_agent_original: The user_agent_original of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterStringSearch
        """

        self._user_agent_original = user_agent_original

    @property
    def user_agent_os_name(self):
        """Gets the user_agent_os_name of this ScreenRecordingFilter.  # noqa: E501


        :return: The user_agent_os_name of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._user_agent_os_name

    @user_agent_os_name.setter
    def user_agent_os_name(self, user_agent_os_name):
        """Sets the user_agent_os_name of this ScreenRecordingFilter.


        :param user_agent_os_name: The user_agent_os_name of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._user_agent_os_name = user_agent_os_name

    @property
    def user_agent_os_version(self):
        """Gets the user_agent_os_version of this ScreenRecordingFilter.  # noqa: E501


        :return: The user_agent_os_version of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._user_agent_os_version

    @user_agent_os_version.setter
    def user_agent_os_version(self, user_agent_os_version):
        """Sets the user_agent_os_version of this ScreenRecordingFilter.


        :param user_agent_os_version: The user_agent_os_version of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._user_agent_os_version = user_agent_os_version

    @property
    def user_ip(self):
        """Gets the user_ip of this ScreenRecordingFilter.  # noqa: E501


        :return: The user_ip of this ScreenRecordingFilter.  # noqa: E501
        :rtype: ScreenRecordingFilterIpSearch
        """
        return self._user_ip

    @user_ip.setter
    def user_ip(self, user_ip):
        """Sets the user_ip of this ScreenRecordingFilter.


        :param user_ip: The user_ip of this ScreenRecordingFilter.  # noqa: E501
        :type: ScreenRecordingFilterIpSearch
        """

        self._user_ip = user_ip

    @property
    def utm_campaign(self):
        """Gets the utm_campaign of this ScreenRecordingFilter.  # noqa: E501


        :return: The utm_campaign of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._utm_campaign

    @utm_campaign.setter
    def utm_campaign(self, utm_campaign):
        """Sets the utm_campaign of this ScreenRecordingFilter.


        :param utm_campaign: The utm_campaign of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._utm_campaign = utm_campaign

    @property
    def utm_source(self):
        """Gets the utm_source of this ScreenRecordingFilter.  # noqa: E501


        :return: The utm_source of this ScreenRecordingFilter.  # noqa: E501
        :rtype: str
        """
        return self._utm_source

    @utm_source.setter
    def utm_source(self, utm_source):
        """Sets the utm_source of this ScreenRecordingFilter.


        :param utm_source: The utm_source of this ScreenRecordingFilter.  # noqa: E501
        :type: str
        """

        self._utm_source = utm_source

    @property
    def visitor_number(self):
        """Gets the visitor_number of this ScreenRecordingFilter.  # noqa: E501


        :return: The visitor_number of this ScreenRecordingFilter.  # noqa: E501
        :rtype: int
        """
        return self._visitor_number

    @visitor_number.setter
    def visitor_number(self, visitor_number):
        """Sets the visitor_number of this ScreenRecordingFilter.


        :param visitor_number: The visitor_number of this ScreenRecordingFilter.  # noqa: E501
        :type: int
        """

        self._visitor_number = visitor_number

    @property
    def watched(self):
        """Gets the watched of this ScreenRecordingFilter.  # noqa: E501


        :return: The watched of this ScreenRecordingFilter.  # noqa: E501
        :rtype: bool
        """
        return self._watched

    @watched.setter
    def watched(self, watched):
        """Sets the watched of this ScreenRecordingFilter.


        :param watched: The watched of this ScreenRecordingFilter.  # noqa: E501
        :type: bool
        """

        self._watched = watched

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
        if issubclass(ScreenRecordingFilter, dict):
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
        if not isinstance(other, ScreenRecordingFilter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
