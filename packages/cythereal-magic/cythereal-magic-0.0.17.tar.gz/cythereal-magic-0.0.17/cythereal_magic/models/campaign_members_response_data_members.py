# coding: utf-8

"""
    Cythereal MAGIC API

     The API for accessing Cythereal MAGIC products and services.  # API Clients  We provide clients in several languages for accessing the MAGIC API. https://bitbucket.org/cythereal/magic-clients  These clients are provided to make integration of the MAGIC API into your existing applications as easy as possible.  If you want to use a language that is not currently supported, please contact us at support@cythereal.com and we will be glad to help.  # Example Inputs  Here are some example inputs that can be used for testing the service:  * Binary SHA1: `ff9790d7902fea4c910b182f6e0b00221a40d616`   * Can be used for `file_hash` parameters. * Procedure RVA: `0x1000`   * Use with the above SHA1 for `proc_rva` parameters.   # API Conventions  Properties MUST be named using `snake_case`.  This API is inspired by the [google json style guide](https://google.github.io/styleguide/jsoncstyleguide.xml). Any questions about conventions not documented here should be addressed by this style guide.  **All responses** MUST be of type `APIResponse` and contain the following fields:  * `api_version` |  The current api version * `success` | Boolean value indicating if the operation succeeded. * `code` | Status code. Typically corresponds to the HTTP status code.  * `message` | A human readable message providing more details about the operation. Can be null or empty.  **Successful operations** MUST return a `SuccessResponse`, which extends `APIResponse` by adding:  * `data` | Properties containing the response object. * `success` | MUST equal True  When returning objects from a successful response, the `data` object SHOULD contain a property named after the requested object type. For example, the `/matches` endpoint should return a response object with `data.matches`. This property SHOULD  contain a list of the returned objects. For the `/matches` endpoint, the `data.matches` property contains a list of MagicMatch objects. See the `/matches` endpoint documentation for an example.  **Failed Operations** MUST return an `ErrorResponse`, which extends `APIResponse` by adding:  * `errors` | Array of error objects. An error object contains the following properties:     * `ErrorObject.reason` | Unique identifier for this error. Example: \"FileNotFoundError\".     * `ErrorObject.message`| Human readable error message. * `success` | MUST equal False.   # noqa: E501

    OpenAPI spec version: 1
    Contact: support@cythereal.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class CampaignMembersResponseDataMembers(object):
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
        'sha1': 'str'
    }

    attribute_map = {
        'sha1': 'sha1'
    }

    def __init__(self, sha1=None):  # noqa: E501
        """CampaignMembersResponseDataMembers - a model defined in Swagger"""  # noqa: E501

        self._sha1 = None
        self.discriminator = None

        if sha1 is not None:
            self.sha1 = sha1

    @property
    def sha1(self):
        """Gets the sha1 of this CampaignMembersResponseDataMembers.  # noqa: E501

        A SHA1 cryptographic hash  # noqa: E501

        :return: The sha1 of this CampaignMembersResponseDataMembers.  # noqa: E501
        :rtype: str
        """
        return self._sha1

    @sha1.setter
    def sha1(self, sha1):
        """Sets the sha1 of this CampaignMembersResponseDataMembers.

        A SHA1 cryptographic hash  # noqa: E501

        :param sha1: The sha1 of this CampaignMembersResponseDataMembers.  # noqa: E501
        :type: str
        """
        if sha1 is not None and not re.search(r'[a-fA-F0-9]{40}', sha1):  # noqa: E501
            raise ValueError(r"Invalid value for `sha1`, must be a follow pattern or equal to `/[a-fA-F0-9]{40}/`")  # noqa: E501

        self._sha1 = sha1

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
        if issubclass(CampaignMembersResponseDataMembers, dict):
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
        if not isinstance(other, CampaignMembersResponseDataMembers):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
