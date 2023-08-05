# coding: utf-8

"""
    MAGIC™ API

    --- # The API for accessing Unknown Cyber MAGIC products and services.  ---  ## Authentication  **(Head to our [/auth](../auth/swagger) api to register, login, or generate a token)**  Supported Authentication Schemes:   * HTTP Basic Authentication  * API-KEY in the `X-API-KEY` request header  * JWT token in the `Authorization:\"Bearer {token}\"` request header  ---  ## Content Negotiation    There are two ways to specify the content type of the response. In order of precedence:     * The **Accept** request header can be set with the desired mime type. The most specific version will prevail. i.e. *application/json* > *application/\\**.       *Accept:\"application/json\"*     * The **format** query parameter. (MUST be in lower case)       *?format=json*    Supported Formats:     | query parameter | Accept Header            |         |    |-----------------|--------------------------|---------|    | **json**        | application/json         | Default |    | **xml**         | application/xml          |         |    | **csv**         | text/csv                 |         |    | **txt**         | text/plain               |         |  --- ## Requests  Supported HTTP Methods:   * **GET**  * **POST**  * **PATCH**  * **DELETE**  * **HEAD**  * **OPTIONS**  Every request supports the following query parameters:   * **explain** - (bool) - Returns a detailed explanation of what the endpoint does, as well as potential query parameters that can be used to customize the results    * **download** - (bool) - If set to a truthy value, acts as setting the 'Content-Disposition' header to *\"attachment;\"* and will download the response as a file.   * **filename** - (str) - The filename to use for a downloaded file. Ignored if no file is being downloaded.        * **format** - (str) - Used in a similar manner to the *Accept* Header. Use this to specify which format you want the response returned in. Defaults to *application/json*. Current acceptable values are:      * **json** - (application/json)     * **xml** - (application/xml)     * **csv** - (text/csv)     * **txt** - (text/plain)         * Custom type that returns a description of usage of the endpoint   * **no_links** - (bool) - If set to a truthy value, links will be disabled from the response   * **uri** - (bool) - If set to a truthy value, id lists will be returned as uris instead of id strings.  ---  ## GET Conventions ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **read_mask** - A list of values (keys) to return for the resource or each resource within the list     * Comma separated string of variables     * Leaving this field blank will return the default values.     * Setting this value equal to **`*`** will include **ALL** possible keys.     * Traversal is allowed with the **`.`** operator.     * There are three special keys that can be used with all endponts         * **`*`** - This will return all possible values available         * **`_self`** - This will include the resources uri         * **`_default`** - This will include all default values (Those given with an empty read_mask)           * This would typically be used in conjunction with other 'non-default' fields       * Ex:         * `_default,family,category,_self`    * **dynamic_mask** - A list of dynamically generated values to return about the resource or each resource within the list     * Comma separated string of variables     * Operates the same as read_mask, but each variable will incur a much greater time cost.     * *May* cause timeouts     * Leaving this field blank or empty will return no dynamic variables.    * **expand_mask** - A list of relational variables to *expand* upon and return more than just the ids     * Comma separated string of variables     * Leaving this field blank will cause all relational data to be returned as a list of ids     * Ex:         * The `children` field for a file may return a list of ids normally, but with `children` set in the           `expand_mask`, it can return a list of child File objects with greater details.  ---  ## POST Conventions  This will create a new resource.  The resource data shall be provided in the request body.  The response will be either a 200 or 201, along with a uri to the newly created resource in the `Location` header.  In the case of a long running job, or reprocess, the response will be a 202 along with a **job_id** and it's corresponding **job_uri** that can be used in the */jobs/* endpoint to see the updated status  ---  ## PATCH Conventions   * The update data shall be provided in the request body.  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **update_mask** - A list of values to update with this request.     * Comma separated string of variables     * This is required to be set for any and all **PATCH** requests to be processed.     * ONLY the specified variables in the update_mask will be updated regardless of the data in the request body.     * An empty or missing *update_mask* **WILL** result in a 400 Bad Request response  ---  ## DELETE Conventions  A successful response will return 204 No Content  ### Possible query parameters:   * **force** - Forces the deletion to go through     * This is required to be set as a truthy value for any and all **DELETE** requests to be processed.     * Not specifying this on a DELETE request (without *explain* set) **WILL** return a 400 Bad Request response   ---  ## *bulk* endpoints  **Bulk** endpoints are the ones that follow the  '*/<resource\\>/bulk/*' convention. They operate in the same fashion as the single resource endpoints ('*/<resource\\>/<resource_id\\>/*') except they can process multiple resources on a single call.  They **MUST** be a **POST** request along with the accompanying request body parameter to work:    * **ids** - A list of ids to operate on (For **GET**, **PATCH**, and **DELETE** bulk requests)   * **resources** - A list of resources to operate on (For **POST** bulk requests)  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available actions)**    * **action** - This is a string and can only be one of four values:      * **GET** - Returns a list of the resources, in the same order as provided in the request body.      * **POST** - Acts the same as a post on the pluralized resource endpoint.         * Instead of an **ids** request body parameter being provided in the request body, a **resources** list of new resources must be provided.      * **PATCH** - Acts the same as a patch on a single resource.          * Follows the same **PATCH** conventions from above*      * **DELETE** - Acts the same as a delete on a single resource.          * Follows the same **DELETE** conventions from above*    * **strict** - Causes the bulk endpoint to fail if a single provided id fails     * Boolean     * If set to True, the bulk call will ONLY operate if it is successful on ALL requested resources.     * If even a single resource is non-existent/forbidden, the call will fail and no side effects will take place.  ---  ## Pagination:  Pagination can be done in combination with sorting and filtering on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Pagination query paramters:        * **page_size** - The number of results to return (default: 50)   * **page_count** - The page used in pagination (default: 1)   * **skip_count** - A specified number of values to skip before collecting values (default: 0)  ---  ## Sorting:  Sorting can be done in combination with filtering and pagination on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Sorting query parameter:   **(Check each endpoint description, or use *explain*, for a list of available sorters)**    * **order_by** - A list of variables to sort the query on     * Comma separated string of variables     * Regex Pattern - `^(-?[\\w]+,?)*$`     * Variables are sorted in ascending order by default     * Prepend the variable with a `-` to change it to descending order     * Multiple sorters can be specified, with precedence matching the order of the parameter     * Ex:         * `-object_class,create_time`  ---  ## Filtering:  Filtering can be done in combination with pagination and sorting on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Filters query parameter:   **(Check each endpoint description, or use *explain*, for a list of available filters)**    * **filters** - A string of filters used to narrow down the query results.     * Semi-colon separated string of variables     * Regex patterns:         * Single filter:             * `^\\ *(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)\\ *`              * `NOT variable__comparator(value)`          * Multiple Filters:             * `^{SINGLE_FILTER_REGEX}(\\ +(AND|OR|;)\\ +{SINGLE_FILTER_REGEX})*$`              * `NOT variable__comparator(value) AND NOT variable__comparator(value); variable__comparator(value)`      * Logical operator order of precedence:         * **AND**         * **OR**         * **;** **(Semi-colon separation denotes conjunction)**         * Example order of precedence:             * **exp1;exp2 AND exp3 OR exp4** is equivalent to **(exp1) AND ((exp2 AND exp3) OR (exp4))**      * Available Comparators:         * **eq** - Equal         * **ne** - Not Equal         * **lt** - Less than         * **lte** - Less than or equal         * **gt** - Greater than         * **gte** - Greater than or equal         * **in** - In (for list values)         * **nin** - Not In (for list values)         * **regex** - Regular Expression Match         * **iregex** - Case Insensitive Regular Expression Match      * The format for **in** and **nin** which operate on arrays is:         * **[]** - The list of values must be enclosed within brackets.         * **,** - The value separtion token is a comma.         * **<variable\\>__<comp\\>([<value1\\>,<value2\\>])**      * Examples:         * `create_time__gte(2022-01-01T13:11:02);object_class__regex(binary.*)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01) AND NOT match_count__gt(10)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01)`  ---  ## Responses  All responses **WILL** be of type `APIResponse` and contain the following fields:  * `success` | Boolean value indicating if the operation succeeded.  * `status` | Status code. Corresponds to the HTTP status code.   * `message` | A human readable message providing more details about the operation.  * `links` | A dictionary of `name`: `uri` links providing navigation and state-based actions on resources  * `errors` | Array of error objects. An error object contains the following properties:      * `reason` | Unique identifier for this error. Ex: \"FileNotFoundError\".      * `message`| Human readable error message.      * `parameter`| The parameter (if any) that caused the issue.  Successful operations **MUST** return a `SuccessResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal True  * `resource` | Properties containing the response object.     * (In the case of a single entity being returned)  **OR**  * `resources` | A list of response objects.     * (In the case of a list of entities being returned)  Failed Operations **MUST** return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal False.  Common Failed Operations that you may hit on any of the endpoint operations:  * 400 - Bad Request - The request is malformed  * 401 - Unauthorized - All endpoints require authorization  * 403 - Forbidden - The endpoint (with the given parameters) is not available to you  * 404 - Not Found - The endpoint doesn't exist, or the resource being searched for doesn't exist  ---  ## Example Inputs  Here are some example inputs that can be used for testing the service:  * `binary_id`: **ff9790d7902fea4c910b182f6e0b00221a40d616**  * `proc_rva`: **0x1000**  * `search_query`: **ransomware**  ---   # noqa: E501

    OpenAPI spec version: 2.0.0 (v2)
    Contact: support@unknowncyber.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class FileGenomicsResponse(object):
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
        'md5': 'str',
        'sha256': 'str',
        'sha512': 'str',
        'image_base': 'str',
        'tags': 'list[str]',
        'notes': 'list[str]',
        'id': 'str',
        'version': 'str',
        'procedure_count': 'int',
        'block_count': 'int',
        'code_count': 'int',
        'semantics_count': 'int',
        'procedures': 'list[ExtendedProcedureResponse]'
    }

    attribute_map = {
        'md5': 'md5',
        'sha256': 'sha256',
        'sha512': 'sha512',
        'image_base': 'image_base',
        'tags': 'tags',
        'notes': 'notes',
        'id': '_id',
        'version': 'version',
        'procedure_count': 'procedure_count',
        'block_count': 'block_count',
        'code_count': 'code_count',
        'semantics_count': 'semantics_count',
        'procedures': 'procedures'
    }

    def __init__(self, md5='99d496fca92daf42fa16d2b2e9a32d19', sha256='1f1bb6c0c4458557780f074d76ffcb3e2ecd3f16ee0d5f70d083a13b03fe7980', sha512='e3918b107dd3eff37edd6265537285b31aee27da2569abcb66649b3982dcbe6175dbc3a38b121066f41f21e6e8a930a9f0f24a98383af5168c5a468ffc8a0824', image_base='0x400000', tags=None, notes=None, id='ce46741bf67591f5f60b7a74dec3ef8d648ca9c6', version='4.0.0', procedure_count=3, block_count=3, code_count=3, semantics_count=3, procedures=None):  # noqa: E501
        """FileGenomicsResponse - a model defined in Swagger"""  # noqa: E501
        self._md5 = None
        self._sha256 = None
        self._sha512 = None
        self._image_base = None
        self._tags = None
        self._notes = None
        self._id = None
        self._version = None
        self._procedure_count = None
        self._block_count = None
        self._code_count = None
        self._semantics_count = None
        self._procedures = None
        self.discriminator = None
        if md5 is not None:
            self.md5 = md5
        if sha256 is not None:
            self.sha256 = sha256
        if sha512 is not None:
            self.sha512 = sha512
        if image_base is not None:
            self.image_base = image_base
        if tags is not None:
            self.tags = tags
        if notes is not None:
            self.notes = notes
        if id is not None:
            self.id = id
        if version is not None:
            self.version = version
        if procedure_count is not None:
            self.procedure_count = procedure_count
        if block_count is not None:
            self.block_count = block_count
        if code_count is not None:
            self.code_count = code_count
        if semantics_count is not None:
            self.semantics_count = semantics_count
        if procedures is not None:
            self.procedures = procedures

    @property
    def md5(self):
        """Gets the md5 of this FileGenomicsResponse.  # noqa: E501


        :return: The md5 of this FileGenomicsResponse.  # noqa: E501
        :rtype: str
        """
        return self._md5

    @md5.setter
    def md5(self, md5):
        """Sets the md5 of this FileGenomicsResponse.


        :param md5: The md5 of this FileGenomicsResponse.  # noqa: E501
        :type: str
        """

        self._md5 = md5

    @property
    def sha256(self):
        """Gets the sha256 of this FileGenomicsResponse.  # noqa: E501


        :return: The sha256 of this FileGenomicsResponse.  # noqa: E501
        :rtype: str
        """
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        """Sets the sha256 of this FileGenomicsResponse.


        :param sha256: The sha256 of this FileGenomicsResponse.  # noqa: E501
        :type: str
        """

        self._sha256 = sha256

    @property
    def sha512(self):
        """Gets the sha512 of this FileGenomicsResponse.  # noqa: E501


        :return: The sha512 of this FileGenomicsResponse.  # noqa: E501
        :rtype: str
        """
        return self._sha512

    @sha512.setter
    def sha512(self, sha512):
        """Sets the sha512 of this FileGenomicsResponse.


        :param sha512: The sha512 of this FileGenomicsResponse.  # noqa: E501
        :type: str
        """

        self._sha512 = sha512

    @property
    def image_base(self):
        """Gets the image_base of this FileGenomicsResponse.  # noqa: E501


        :return: The image_base of this FileGenomicsResponse.  # noqa: E501
        :rtype: str
        """
        return self._image_base

    @image_base.setter
    def image_base(self, image_base):
        """Sets the image_base of this FileGenomicsResponse.


        :param image_base: The image_base of this FileGenomicsResponse.  # noqa: E501
        :type: str
        """

        self._image_base = image_base

    @property
    def tags(self):
        """Gets the tags of this FileGenomicsResponse.  # noqa: E501


        :return: The tags of this FileGenomicsResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this FileGenomicsResponse.


        :param tags: The tags of this FileGenomicsResponse.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def notes(self):
        """Gets the notes of this FileGenomicsResponse.  # noqa: E501


        :return: The notes of this FileGenomicsResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this FileGenomicsResponse.


        :param notes: The notes of this FileGenomicsResponse.  # noqa: E501
        :type: list[str]
        """

        self._notes = notes

    @property
    def id(self):
        """Gets the id of this FileGenomicsResponse.  # noqa: E501


        :return: The id of this FileGenomicsResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FileGenomicsResponse.


        :param id: The id of this FileGenomicsResponse.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def version(self):
        """Gets the version of this FileGenomicsResponse.  # noqa: E501


        :return: The version of this FileGenomicsResponse.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this FileGenomicsResponse.


        :param version: The version of this FileGenomicsResponse.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def procedure_count(self):
        """Gets the procedure_count of this FileGenomicsResponse.  # noqa: E501


        :return: The procedure_count of this FileGenomicsResponse.  # noqa: E501
        :rtype: int
        """
        return self._procedure_count

    @procedure_count.setter
    def procedure_count(self, procedure_count):
        """Sets the procedure_count of this FileGenomicsResponse.


        :param procedure_count: The procedure_count of this FileGenomicsResponse.  # noqa: E501
        :type: int
        """

        self._procedure_count = procedure_count

    @property
    def block_count(self):
        """Gets the block_count of this FileGenomicsResponse.  # noqa: E501


        :return: The block_count of this FileGenomicsResponse.  # noqa: E501
        :rtype: int
        """
        return self._block_count

    @block_count.setter
    def block_count(self, block_count):
        """Sets the block_count of this FileGenomicsResponse.


        :param block_count: The block_count of this FileGenomicsResponse.  # noqa: E501
        :type: int
        """

        self._block_count = block_count

    @property
    def code_count(self):
        """Gets the code_count of this FileGenomicsResponse.  # noqa: E501


        :return: The code_count of this FileGenomicsResponse.  # noqa: E501
        :rtype: int
        """
        return self._code_count

    @code_count.setter
    def code_count(self, code_count):
        """Sets the code_count of this FileGenomicsResponse.


        :param code_count: The code_count of this FileGenomicsResponse.  # noqa: E501
        :type: int
        """

        self._code_count = code_count

    @property
    def semantics_count(self):
        """Gets the semantics_count of this FileGenomicsResponse.  # noqa: E501


        :return: The semantics_count of this FileGenomicsResponse.  # noqa: E501
        :rtype: int
        """
        return self._semantics_count

    @semantics_count.setter
    def semantics_count(self, semantics_count):
        """Sets the semantics_count of this FileGenomicsResponse.


        :param semantics_count: The semantics_count of this FileGenomicsResponse.  # noqa: E501
        :type: int
        """

        self._semantics_count = semantics_count

    @property
    def procedures(self):
        """Gets the procedures of this FileGenomicsResponse.  # noqa: E501


        :return: The procedures of this FileGenomicsResponse.  # noqa: E501
        :rtype: list[ExtendedProcedureResponse]
        """
        return self._procedures

    @procedures.setter
    def procedures(self, procedures):
        """Sets the procedures of this FileGenomicsResponse.


        :param procedures: The procedures of this FileGenomicsResponse.  # noqa: E501
        :type: list[ExtendedProcedureResponse]
        """

        self._procedures = procedures

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
        if issubclass(FileGenomicsResponse, dict):
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
        if not isinstance(other, FileGenomicsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
