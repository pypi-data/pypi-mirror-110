# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.0.1210
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class RoleResponse(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'id': 'RoleId',
        'role_hierarchy_index': 'int',
        'description': 'str',
        'resource': 'RoleResourceRequest',
        'when': 'WhenSpec',
        'permission': 'str',
        'limit': 'dict(str, str)',
        'links': 'list[Link]'
    }

    attribute_map = {
        'id': 'id',
        'role_hierarchy_index': 'roleHierarchyIndex',
        'description': 'description',
        'resource': 'resource',
        'when': 'when',
        'permission': 'permission',
        'limit': 'limit',
        'links': 'links'
    }

    required_map = {
        'id': 'required',
        'role_hierarchy_index': 'required',
        'description': 'optional',
        'resource': 'required',
        'when': 'required',
        'permission': 'required',
        'limit': 'optional',
        'links': 'optional'
    }

    def __init__(self, id=None, role_hierarchy_index=None, description=None, resource=None, when=None, permission=None, limit=None, links=None):  # noqa: E501
        """
        RoleResponse - a model defined in OpenAPI

        :param id:  (required)
        :type id: finbourne_access.RoleId
        :param role_hierarchy_index:  (required)
        :type role_hierarchy_index: int
        :param description: 
        :type description: str
        :param resource:  (required)
        :type resource: finbourne_access.RoleResourceRequest
        :param when:  (required)
        :type when: finbourne_access.WhenSpec
        :param permission:  (required)
        :type permission: str
        :param limit: 
        :type limit: dict(str, str)
        :param links: 
        :type links: list[finbourne_access.Link]

        """  # noqa: E501

        self._id = None
        self._role_hierarchy_index = None
        self._description = None
        self._resource = None
        self._when = None
        self._permission = None
        self._limit = None
        self._links = None
        self.discriminator = None

        self.id = id
        self.role_hierarchy_index = role_hierarchy_index
        self.description = description
        self.resource = resource
        self.when = when
        self.permission = permission
        self.limit = limit
        self.links = links

    @property
    def id(self):
        """Gets the id of this RoleResponse.  # noqa: E501


        :return: The id of this RoleResponse.  # noqa: E501
        :rtype: RoleId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this RoleResponse.


        :param id: The id of this RoleResponse.  # noqa: E501
        :type: RoleId
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def role_hierarchy_index(self):
        """Gets the role_hierarchy_index of this RoleResponse.  # noqa: E501


        :return: The role_hierarchy_index of this RoleResponse.  # noqa: E501
        :rtype: int
        """
        return self._role_hierarchy_index

    @role_hierarchy_index.setter
    def role_hierarchy_index(self, role_hierarchy_index):
        """Sets the role_hierarchy_index of this RoleResponse.


        :param role_hierarchy_index: The role_hierarchy_index of this RoleResponse.  # noqa: E501
        :type: int
        """
        if role_hierarchy_index is None:
            raise ValueError("Invalid value for `role_hierarchy_index`, must not be `None`")  # noqa: E501

        self._role_hierarchy_index = role_hierarchy_index

    @property
    def description(self):
        """Gets the description of this RoleResponse.  # noqa: E501


        :return: The description of this RoleResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this RoleResponse.


        :param description: The description of this RoleResponse.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def resource(self):
        """Gets the resource of this RoleResponse.  # noqa: E501


        :return: The resource of this RoleResponse.  # noqa: E501
        :rtype: RoleResourceRequest
        """
        return self._resource

    @resource.setter
    def resource(self, resource):
        """Sets the resource of this RoleResponse.


        :param resource: The resource of this RoleResponse.  # noqa: E501
        :type: RoleResourceRequest
        """
        if resource is None:
            raise ValueError("Invalid value for `resource`, must not be `None`")  # noqa: E501

        self._resource = resource

    @property
    def when(self):
        """Gets the when of this RoleResponse.  # noqa: E501


        :return: The when of this RoleResponse.  # noqa: E501
        :rtype: WhenSpec
        """
        return self._when

    @when.setter
    def when(self, when):
        """Sets the when of this RoleResponse.


        :param when: The when of this RoleResponse.  # noqa: E501
        :type: WhenSpec
        """
        if when is None:
            raise ValueError("Invalid value for `when`, must not be `None`")  # noqa: E501

        self._when = when

    @property
    def permission(self):
        """Gets the permission of this RoleResponse.  # noqa: E501


        :return: The permission of this RoleResponse.  # noqa: E501
        :rtype: str
        """
        return self._permission

    @permission.setter
    def permission(self, permission):
        """Sets the permission of this RoleResponse.


        :param permission: The permission of this RoleResponse.  # noqa: E501
        :type: str
        """
        if permission is None:
            raise ValueError("Invalid value for `permission`, must not be `None`")  # noqa: E501

        self._permission = permission

    @property
    def limit(self):
        """Gets the limit of this RoleResponse.  # noqa: E501


        :return: The limit of this RoleResponse.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this RoleResponse.


        :param limit: The limit of this RoleResponse.  # noqa: E501
        :type: dict(str, str)
        """

        self._limit = limit

    @property
    def links(self):
        """Gets the links of this RoleResponse.  # noqa: E501


        :return: The links of this RoleResponse.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this RoleResponse.


        :param links: The links of this RoleResponse.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        if not isinstance(other, RoleResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
