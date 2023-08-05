# coding: utf-8

"""
    MAGIC™ API

    --- # The API for accessing Cythereal MAGIC products and services.  ---  ## Authentication  **(Head to our [/auth](../auth/swagger) api to register, login, or generate a token)**  Supported Authentication Schemes:   * HTTP Basic Authentication  * API-KEY in the `X-API-KEY` request header  * JWT token in the `Authorization:\"Bearer {token}\"` request header  ---  ## Content Negotiation    There are two ways to specify the content type of the response. In order of precedence:     * The **Accept** request header can be set with the desired mime type. The most specific version will prevail. i.e. *application/json* > *application/\\**.       *Accept:\"application/json\"*     * The **format** query parameter. (MUST be in lower case)       *?format=json*    Supported Formats:     | query parameter | Accept Header            |         |    |-----------------|--------------------------|---------|    | **json**        | application/json         | Default |    | **xml**         | application/xml          |         |    | **csv**         | text/csv                 |         |    | **txt**         | text/plain               |         |  --- ## Requests  Supported HTTP Methods:   * **GET**  * **POST**  * **PATCH**  * **DELETE**  * **HEAD**  * **OPTIONS**  Every request supports the following query parameters:   * **explain** - (bool) - Returns a detailed explanation of what the endpoint does, as well as potential query parameters that can be used to customize the results    * **download** - (bool) - If set to a truthy value, acts as setting the 'Content-Disposition' header to *\"attachment;\"* and will download the response as a file.   * **filename** - (str) - The filename to use for a downloaded file. Ignored if no file is being downloaded.        * **format** - (str) - Used in a similar manner to the *Accept* Header. Use this to specify which format you want the response returned in. Defaults to *application/json*. Current acceptable values are:      * **json** - (application/json)     * **xml** - (application/xml)     * **csv** - (text/csv)     * **txt** - (text/plain)         * Custom type that returns a description of usage of the endpoint   * **no_links** - (bool) - If set to a truthy value, links will be disabled from the response   * **uri** - (bool) - If set to a truthy value, id lists will be returned as uris instead of id strings.  ---  ## GET Conventions ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **read_mask** - A list of values (keys) to return for the resource or each resource within the list     * Comma separated string of variables     * Leaving this field blank will return the default values.     * Setting this value equal to **`*`** will include **ALL** possible keys.     * Traversal is allowed with the **`.`** operator.     * There are three special keys that can be used with all endponts         * **`*`** - This will return all possible values available         * **`_self`** - This will include the resources uri         * **`_default`** - This will include all default values (Those given with an empty read_mask)           * This would typically be used in conjunction with other 'non-default' fields       * Ex:         * `_default,family,category,_self`    * **dynamic_mask** - A list of dynamically generated values to return about the resource or each resource within the list     * Comma separated string of variables     * Operates the same as read_mask, but each variable will incur a much greater time cost.     * *May* cause timeouts     * Leaving this field blank or empty will return no dynamic variables.    * **expand_mask** - A list of relational variables to *expand* upon and return more than just the ids     * Comma separated string of variables     * Leaving this field blank will cause all relational data to be returned as a list of ids     * Ex:         * The `children` field for a file may return a list of ids normally, but with `children` set in the           `expand_mask`, it can return a list of child File objects with greater details.  ---  ## POST Conventions  This will create a new resource.  The resource data shall be provided in the request body.  The response will be either a 200 or 201, along with a uri to the newly created resource in the `Location` header.  In the case of a long running job, or reprocess, the response will be a 202 along with a **job_id** and it's corresponding **job_uri** that can be used in the */jobs/* endpoint to see the updated status  ---  ## PATCH Conventions   * The update data shall be provided in the request body.  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **update_mask** - A list of values to update with this request.     * Comma separated string of variables     * This is required to be set for any and all **PATCH** requests to be processed.     * ONLY the specified variables in the update_mask will be updated regardless of the data in the request body.     * An empty or missing *update_mask* **WILL** result in a 400 Bad Request response  ---  ## DELETE Conventions  A successful response will return 204 No Content  ### Possible query parameters:   * **force** - Forces the deletion to go through     * This is required to be set as a truthy value for any and all **DELETE** requests to be processed.     * Not specifying this on a DELETE request (without *explain* set) **WILL** return a 400 Bad Request response   ---  ## *bulk* endpoints  **Bulk** endpoints are the ones that follow the  '*/<resource\\>/bulk/*' convention. They operate in the same fashion as the single resource endpoints ('*/<resource\\>/<resource_id\\>/*') except they can process multiple resources on a single call.  They **MUST** be a **POST** request along with the accompanying request body parameter to work:    * **ids** - A list of ids to operate on (For **GET**, **PATCH**, and **DELETE** bulk requests)   * **resources** - A list of resources to operate on (For **POST** bulk requests)  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available actions)**    * **action** - This is a string and can only be one of four values:      * **GET** - Returns a list of the resources, in the same order as provided in the request body.      * **POST** - Acts the same as a post on the pluralized resource endpoint.         * Instead of an **ids** request body parameter being provided in the request body, a **resources** list of new resources must be provided.      * **PATCH** - Acts the same as a patch on a single resource.          * Follows the same **PATCH** conventions from above*      * **DELETE** - Acts the same as a delete on a single resource.          * Follows the same **DELETE** conventions from above*    * **strict** - Causes the bulk endpoint to fail if a single provided id fails     * Boolean     * If set to True, the bulk call will ONLY operate if it is successful on ALL requested resources.     * If even a single resource is non-existent/forbidden, the call will fail and no side effects will take place.  ---  ## Pagination:  Pagination can be done in combination with sorting and filtering on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Pagination query paramters:        * **page_size** - The number of results to return (default: 50)   * **page_count** - The page used in pagination (default: 1)   * **skip_count** - A specified number of values to skip before collecting values (default: 0)  ---  ## Sorting:  Sorting can be done in combination with filtering and pagination on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Sorting query parameter:   **(Check each endpoint description, or use *explain*, for a list of available sorters)**    * **order_by** - A list of variables to sort the query on     * Comma separated string of variables     * Regex Pattern - `^(-?[\\w]+,?)*$`     * Variables are sorted in ascending order by default     * Prepend the variable with a `-` to change it to descending order     * Multiple sorters can be specified, with precedence matching the order of the parameter     * Ex:         * `-object_class,create_time`  ---  ## Filtering:  Filtering can be done in combination with pagination and sorting on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Filters query parameter:   **(Check each endpoint description, or use *explain*, for a list of available filters)**    * **filters** - A string of filters used to narrow down the query results.     * Semi-colon separated string of variables     * Regex patterns:         * Single filter:             * `^\\ *(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)\\ *`              * `NOT variable__comparator(value)`          * Multiple Filters:             * `^{SINGLE_FILTER_REGEX}(\\ +(AND|OR|;)\\ +{SINGLE_FILTER_REGEX})*$`              * `NOT variable__comparator(value) AND NOT variable__comparator(value); variable__comparator(value)`      * Logical operator order of precedence:         * **AND**         * **OR**         * **;** **(Semi-colon separation denotes conjunction)**         * Example order of precedence:             * **exp1;exp2 AND exp3 OR exp4** is equivalent to **(exp1) AND ((exp2 AND exp3) OR (exp4))**      * Available Comparators:         * **eq** - Equal         * **ne** - Not Equal         * **lt** - Less than         * **lte** - Less than or equal         * **gt** - Greater than         * **gte** - Greater than or equal         * **in** - In (for list values)         * **nin** - Not In (for list values)         * **regex** - Regular Expression Match         * **iregex** - Case Insensitive Regular Expression Match      * The format for **in** and **nin** which operate on arrays is:         * **[]** - The list of values must be enclosed within brackets.         * **,** - The value separtion token is a comma.         * **<variable\\>__<comp\\>([<value1\\>,<value2\\>])**      * Examples:         * `create_time__gte(2022-01-01T13:11:02);object_class__regex(binary.*)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01) AND NOT match_count__gt(10)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01)`  ---  ## Responses  All responses **WILL** be of type `APIResponse` and contain the following fields:  * `success` | Boolean value indicating if the operation succeeded.  * `status` | Status code. Corresponds to the HTTP status code.   * `message` | A human readable message providing more details about the operation.  * `links` | A dictionary of `name`: `uri` links providing navigation and state-based actions on resources  * `errors` | Array of error objects. An error object contains the following properties:      * `reason` | Unique identifier for this error. Ex: \"FileNotFoundError\".      * `message`| Human readable error message.      * `parameter`| The parameter (if any) that caused the issue.  Successful operations **MUST** return a `SuccessResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal True  * `resource` | Properties containing the response object.     * (In the case of a single entity being returned)  **OR**  * `resources` | A list of response objects.     * (In the case of a list of entities being returned)  Failed Operations **MUST** return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal False.  Common Failed Operations that you may hit on any of the endpoint operations:  * 400 - Bad Request - The request is malformed  * 401 - Unauthorized - All endpoints require authorization  * 403 - Forbidden - The endpoint (with the given parameters) is not available to you  * 404 - Not Found - The endpoint doesn't exist, or the resource being searched for doesn't exist  ---  ## Example Inputs  Here are some example inputs that can be used for testing the service:  * `binary_id`: **ff9790d7902fea4c910b182f6e0b00221a40d616**  * `proc_rva`: **0x1000**  * `search_query`: **ransomware**  ---   # noqa: E501

    OpenAPI spec version: 2.0.0 (v2)
    Contact: support@cythereal.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ProcedureSchema(object):
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
        'tags': 'list[str]',
        'notes': 'list[str]',
        'proc_hash': 'str',
        'variant_hash': 'str',
        'binary_id': 'str',
        'start_ea': 'str',
        'end_ea': 'str',
        'procedure_segment': 'str',
        'is_libary': 'bool',
        'is_thunk': 'bool',
        'strings': 'list[str]',
        'api_calls': 'list[str]',
        'block_count': 'int',
        'code_count': 'int',
        'semantics_count': 'int',
        'version': 'str',
        'procedure_id': 'str',
        'blocks': 'list[BlockSchema]',
        'cfg': 'dict(str, list[str])'
    }

    attribute_map = {
        'tags': 'tags',
        'notes': 'notes',
        'proc_hash': 'proc_hash',
        'variant_hash': 'variant_hash',
        'binary_id': 'binary_id',
        'start_ea': 'startEA',
        'end_ea': 'endEA',
        'procedure_segment': 'procedure_segment',
        'is_libary': 'is_libary',
        'is_thunk': 'is_thunk',
        'strings': 'strings',
        'api_calls': 'api_calls',
        'block_count': 'block_count',
        'code_count': 'code_count',
        'semantics_count': 'semantics_count',
        'version': 'version',
        'procedure_id': 'procedure_id',
        'blocks': 'blocks',
        'cfg': 'cfg'
    }

    def __init__(self, tags=None, notes=None, proc_hash='ecb50f092ebeeac4cf7804f8273d90e1', variant_hash='bd0b14a2273f3856c566d5a0c5c81488', binary_id='ce46741bf67591f5f60b7a74dec3ef8d648ca9c6', start_ea='0x1000', end_ea='0x101d', procedure_segment='.text', is_libary=False, is_thunk=False, strings=None, api_calls=None, block_count=1, code_count=3, semantics_count=7, version='4.0.0', procedure_id='ce46741bf67591f5f60b7a74dec3ef8d648ca9c6/0x1000', blocks=None, cfg=None):  # noqa: E501
        """ProcedureSchema - a model defined in Swagger"""  # noqa: E501
        self._tags = None
        self._notes = None
        self._proc_hash = None
        self._variant_hash = None
        self._binary_id = None
        self._start_ea = None
        self._end_ea = None
        self._procedure_segment = None
        self._is_libary = None
        self._is_thunk = None
        self._strings = None
        self._api_calls = None
        self._block_count = None
        self._code_count = None
        self._semantics_count = None
        self._version = None
        self._procedure_id = None
        self._blocks = None
        self._cfg = None
        self.discriminator = None
        if tags is not None:
            self.tags = tags
        if notes is not None:
            self.notes = notes
        if proc_hash is not None:
            self.proc_hash = proc_hash
        if variant_hash is not None:
            self.variant_hash = variant_hash
        if binary_id is not None:
            self.binary_id = binary_id
        if start_ea is not None:
            self.start_ea = start_ea
        if end_ea is not None:
            self.end_ea = end_ea
        if procedure_segment is not None:
            self.procedure_segment = procedure_segment
        if is_libary is not None:
            self.is_libary = is_libary
        if is_thunk is not None:
            self.is_thunk = is_thunk
        if strings is not None:
            self.strings = strings
        if api_calls is not None:
            self.api_calls = api_calls
        if block_count is not None:
            self.block_count = block_count
        if code_count is not None:
            self.code_count = code_count
        if semantics_count is not None:
            self.semantics_count = semantics_count
        if version is not None:
            self.version = version
        if procedure_id is not None:
            self.procedure_id = procedure_id
        if blocks is not None:
            self.blocks = blocks
        self.cfg = cfg

    @property
    def tags(self):
        """Gets the tags of this ProcedureSchema.  # noqa: E501


        :return: The tags of this ProcedureSchema.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ProcedureSchema.


        :param tags: The tags of this ProcedureSchema.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def notes(self):
        """Gets the notes of this ProcedureSchema.  # noqa: E501


        :return: The notes of this ProcedureSchema.  # noqa: E501
        :rtype: list[str]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this ProcedureSchema.


        :param notes: The notes of this ProcedureSchema.  # noqa: E501
        :type: list[str]
        """

        self._notes = notes

    @property
    def proc_hash(self):
        """Gets the proc_hash of this ProcedureSchema.  # noqa: E501


        :return: The proc_hash of this ProcedureSchema.  # noqa: E501
        :rtype: str
        """
        return self._proc_hash

    @proc_hash.setter
    def proc_hash(self, proc_hash):
        """Sets the proc_hash of this ProcedureSchema.


        :param proc_hash: The proc_hash of this ProcedureSchema.  # noqa: E501
        :type: str
        """

        self._proc_hash = proc_hash

    @property
    def variant_hash(self):
        """Gets the variant_hash of this ProcedureSchema.  # noqa: E501


        :return: The variant_hash of this ProcedureSchema.  # noqa: E501
        :rtype: str
        """
        return self._variant_hash

    @variant_hash.setter
    def variant_hash(self, variant_hash):
        """Sets the variant_hash of this ProcedureSchema.


        :param variant_hash: The variant_hash of this ProcedureSchema.  # noqa: E501
        :type: str
        """

        self._variant_hash = variant_hash

    @property
    def binary_id(self):
        """Gets the binary_id of this ProcedureSchema.  # noqa: E501


        :return: The binary_id of this ProcedureSchema.  # noqa: E501
        :rtype: str
        """
        return self._binary_id

    @binary_id.setter
    def binary_id(self, binary_id):
        """Sets the binary_id of this ProcedureSchema.


        :param binary_id: The binary_id of this ProcedureSchema.  # noqa: E501
        :type: str
        """

        self._binary_id = binary_id

    @property
    def start_ea(self):
        """Gets the start_ea of this ProcedureSchema.  # noqa: E501


        :return: The start_ea of this ProcedureSchema.  # noqa: E501
        :rtype: str
        """
        return self._start_ea

    @start_ea.setter
    def start_ea(self, start_ea):
        """Sets the start_ea of this ProcedureSchema.


        :param start_ea: The start_ea of this ProcedureSchema.  # noqa: E501
        :type: str
        """

        self._start_ea = start_ea

    @property
    def end_ea(self):
        """Gets the end_ea of this ProcedureSchema.  # noqa: E501


        :return: The end_ea of this ProcedureSchema.  # noqa: E501
        :rtype: str
        """
        return self._end_ea

    @end_ea.setter
    def end_ea(self, end_ea):
        """Sets the end_ea of this ProcedureSchema.


        :param end_ea: The end_ea of this ProcedureSchema.  # noqa: E501
        :type: str
        """

        self._end_ea = end_ea

    @property
    def procedure_segment(self):
        """Gets the procedure_segment of this ProcedureSchema.  # noqa: E501


        :return: The procedure_segment of this ProcedureSchema.  # noqa: E501
        :rtype: str
        """
        return self._procedure_segment

    @procedure_segment.setter
    def procedure_segment(self, procedure_segment):
        """Sets the procedure_segment of this ProcedureSchema.


        :param procedure_segment: The procedure_segment of this ProcedureSchema.  # noqa: E501
        :type: str
        """

        self._procedure_segment = procedure_segment

    @property
    def is_libary(self):
        """Gets the is_libary of this ProcedureSchema.  # noqa: E501


        :return: The is_libary of this ProcedureSchema.  # noqa: E501
        :rtype: bool
        """
        return self._is_libary

    @is_libary.setter
    def is_libary(self, is_libary):
        """Sets the is_libary of this ProcedureSchema.


        :param is_libary: The is_libary of this ProcedureSchema.  # noqa: E501
        :type: bool
        """

        self._is_libary = is_libary

    @property
    def is_thunk(self):
        """Gets the is_thunk of this ProcedureSchema.  # noqa: E501


        :return: The is_thunk of this ProcedureSchema.  # noqa: E501
        :rtype: bool
        """
        return self._is_thunk

    @is_thunk.setter
    def is_thunk(self, is_thunk):
        """Sets the is_thunk of this ProcedureSchema.


        :param is_thunk: The is_thunk of this ProcedureSchema.  # noqa: E501
        :type: bool
        """

        self._is_thunk = is_thunk

    @property
    def strings(self):
        """Gets the strings of this ProcedureSchema.  # noqa: E501


        :return: The strings of this ProcedureSchema.  # noqa: E501
        :rtype: list[str]
        """
        return self._strings

    @strings.setter
    def strings(self, strings):
        """Sets the strings of this ProcedureSchema.


        :param strings: The strings of this ProcedureSchema.  # noqa: E501
        :type: list[str]
        """

        self._strings = strings

    @property
    def api_calls(self):
        """Gets the api_calls of this ProcedureSchema.  # noqa: E501


        :return: The api_calls of this ProcedureSchema.  # noqa: E501
        :rtype: list[str]
        """
        return self._api_calls

    @api_calls.setter
    def api_calls(self, api_calls):
        """Sets the api_calls of this ProcedureSchema.


        :param api_calls: The api_calls of this ProcedureSchema.  # noqa: E501
        :type: list[str]
        """

        self._api_calls = api_calls

    @property
    def block_count(self):
        """Gets the block_count of this ProcedureSchema.  # noqa: E501


        :return: The block_count of this ProcedureSchema.  # noqa: E501
        :rtype: int
        """
        return self._block_count

    @block_count.setter
    def block_count(self, block_count):
        """Sets the block_count of this ProcedureSchema.


        :param block_count: The block_count of this ProcedureSchema.  # noqa: E501
        :type: int
        """

        self._block_count = block_count

    @property
    def code_count(self):
        """Gets the code_count of this ProcedureSchema.  # noqa: E501


        :return: The code_count of this ProcedureSchema.  # noqa: E501
        :rtype: int
        """
        return self._code_count

    @code_count.setter
    def code_count(self, code_count):
        """Sets the code_count of this ProcedureSchema.


        :param code_count: The code_count of this ProcedureSchema.  # noqa: E501
        :type: int
        """

        self._code_count = code_count

    @property
    def semantics_count(self):
        """Gets the semantics_count of this ProcedureSchema.  # noqa: E501


        :return: The semantics_count of this ProcedureSchema.  # noqa: E501
        :rtype: int
        """
        return self._semantics_count

    @semantics_count.setter
    def semantics_count(self, semantics_count):
        """Sets the semantics_count of this ProcedureSchema.


        :param semantics_count: The semantics_count of this ProcedureSchema.  # noqa: E501
        :type: int
        """

        self._semantics_count = semantics_count

    @property
    def version(self):
        """Gets the version of this ProcedureSchema.  # noqa: E501


        :return: The version of this ProcedureSchema.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ProcedureSchema.


        :param version: The version of this ProcedureSchema.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def procedure_id(self):
        """Gets the procedure_id of this ProcedureSchema.  # noqa: E501


        :return: The procedure_id of this ProcedureSchema.  # noqa: E501
        :rtype: str
        """
        return self._procedure_id

    @procedure_id.setter
    def procedure_id(self, procedure_id):
        """Sets the procedure_id of this ProcedureSchema.


        :param procedure_id: The procedure_id of this ProcedureSchema.  # noqa: E501
        :type: str
        """

        self._procedure_id = procedure_id

    @property
    def blocks(self):
        """Gets the blocks of this ProcedureSchema.  # noqa: E501


        :return: The blocks of this ProcedureSchema.  # noqa: E501
        :rtype: list[BlockSchema]
        """
        return self._blocks

    @blocks.setter
    def blocks(self, blocks):
        """Sets the blocks of this ProcedureSchema.


        :param blocks: The blocks of this ProcedureSchema.  # noqa: E501
        :type: list[BlockSchema]
        """

        self._blocks = blocks

    @property
    def cfg(self):
        """Gets the cfg of this ProcedureSchema.  # noqa: E501


        :return: The cfg of this ProcedureSchema.  # noqa: E501
        :rtype: dict(str, list[str])
        """
        return self._cfg

    @cfg.setter
    def cfg(self, cfg):
        """Sets the cfg of this ProcedureSchema.


        :param cfg: The cfg of this ProcedureSchema.  # noqa: E501
        :type: dict(str, list[str])
        """
        if cfg is None:
            raise ValueError("Invalid value for `cfg`, must not be `None`")  # noqa: E501

        self._cfg = cfg

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
        if issubclass(ProcedureSchema, dict):
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
        if not isinstance(other, ProcedureSchema):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
