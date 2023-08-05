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

class FileProcedures(object):
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
        'hard_hash': 'str',
        'status': 'str',
        'signature': 'list[list[str]]',
        'example_procedure_id': 'str',
        'example_procedure': 'list[list[str]]',
        'example_block_eas': 'list[ProcedureBlock]',
        'example_start_ea': 'str',
        'example_end_ea': 'str',
        'is_library': 'bool',
        'block_counts': 'list[int]',
        'instr_counts': 'list[int]',
        'byte_counts': 'list[int]',
        'occurrence_counts': 'int',
        'name_counts': 'int',
        'procedure_names': 'list[str]',
        'coverage': 'float',
        'signature_count': 'int',
        'example_procedure_count': 'int'
    }

    attribute_map = {
        'hard_hash': 'hard_hash',
        'status': 'status',
        'signature': 'signature',
        'example_procedure_id': 'example_procedure_id',
        'example_procedure': 'example_procedure',
        'example_block_eas': 'example_blockEAs',
        'example_start_ea': 'example_startEA',
        'example_end_ea': 'example_endEA',
        'is_library': 'is_library',
        'block_counts': 'block_counts',
        'instr_counts': 'instr_counts',
        'byte_counts': 'byte_counts',
        'occurrence_counts': 'occurrence_counts',
        'name_counts': 'name_counts',
        'procedure_names': 'procedure_names',
        'coverage': 'coverage',
        'signature_count': 'signature_count',
        'example_procedure_count': 'example_procedure_count'
    }

    def __init__(self, hard_hash=None, status=None, signature=None, example_procedure_id=None, example_procedure=None, example_block_eas=None, example_start_ea=None, example_end_ea=None, is_library=None, block_counts=None, instr_counts=None, byte_counts=None, occurrence_counts=None, name_counts=None, procedure_names=None, coverage=None, signature_count=None, example_procedure_count=None):  # noqa: E501
        """FileProcedures - a model defined in Swagger"""  # noqa: E501
        self._hard_hash = None
        self._status = None
        self._signature = None
        self._example_procedure_id = None
        self._example_procedure = None
        self._example_block_eas = None
        self._example_start_ea = None
        self._example_end_ea = None
        self._is_library = None
        self._block_counts = None
        self._instr_counts = None
        self._byte_counts = None
        self._occurrence_counts = None
        self._name_counts = None
        self._procedure_names = None
        self._coverage = None
        self._signature_count = None
        self._example_procedure_count = None
        self.discriminator = None
        if hard_hash is not None:
            self.hard_hash = hard_hash
        if status is not None:
            self.status = status
        if signature is not None:
            self.signature = signature
        if example_procedure_id is not None:
            self.example_procedure_id = example_procedure_id
        if example_procedure is not None:
            self.example_procedure = example_procedure
        if example_block_eas is not None:
            self.example_block_eas = example_block_eas
        if example_start_ea is not None:
            self.example_start_ea = example_start_ea
        if example_end_ea is not None:
            self.example_end_ea = example_end_ea
        if is_library is not None:
            self.is_library = is_library
        if block_counts is not None:
            self.block_counts = block_counts
        if instr_counts is not None:
            self.instr_counts = instr_counts
        if byte_counts is not None:
            self.byte_counts = byte_counts
        if occurrence_counts is not None:
            self.occurrence_counts = occurrence_counts
        if name_counts is not None:
            self.name_counts = name_counts
        if procedure_names is not None:
            self.procedure_names = procedure_names
        if coverage is not None:
            self.coverage = coverage
        if signature_count is not None:
            self.signature_count = signature_count
        if example_procedure_count is not None:
            self.example_procedure_count = example_procedure_count

    @property
    def hard_hash(self):
        """Gets the hard_hash of this FileProcedures.  # noqa: E501


        :return: The hard_hash of this FileProcedures.  # noqa: E501
        :rtype: str
        """
        return self._hard_hash

    @hard_hash.setter
    def hard_hash(self, hard_hash):
        """Sets the hard_hash of this FileProcedures.


        :param hard_hash: The hard_hash of this FileProcedures.  # noqa: E501
        :type: str
        """

        self._hard_hash = hard_hash

    @property
    def status(self):
        """Gets the status of this FileProcedures.  # noqa: E501


        :return: The status of this FileProcedures.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this FileProcedures.


        :param status: The status of this FileProcedures.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def signature(self):
        """Gets the signature of this FileProcedures.  # noqa: E501


        :return: The signature of this FileProcedures.  # noqa: E501
        :rtype: list[list[str]]
        """
        return self._signature

    @signature.setter
    def signature(self, signature):
        """Sets the signature of this FileProcedures.


        :param signature: The signature of this FileProcedures.  # noqa: E501
        :type: list[list[str]]
        """

        self._signature = signature

    @property
    def example_procedure_id(self):
        """Gets the example_procedure_id of this FileProcedures.  # noqa: E501


        :return: The example_procedure_id of this FileProcedures.  # noqa: E501
        :rtype: str
        """
        return self._example_procedure_id

    @example_procedure_id.setter
    def example_procedure_id(self, example_procedure_id):
        """Sets the example_procedure_id of this FileProcedures.


        :param example_procedure_id: The example_procedure_id of this FileProcedures.  # noqa: E501
        :type: str
        """

        self._example_procedure_id = example_procedure_id

    @property
    def example_procedure(self):
        """Gets the example_procedure of this FileProcedures.  # noqa: E501


        :return: The example_procedure of this FileProcedures.  # noqa: E501
        :rtype: list[list[str]]
        """
        return self._example_procedure

    @example_procedure.setter
    def example_procedure(self, example_procedure):
        """Sets the example_procedure of this FileProcedures.


        :param example_procedure: The example_procedure of this FileProcedures.  # noqa: E501
        :type: list[list[str]]
        """

        self._example_procedure = example_procedure

    @property
    def example_block_eas(self):
        """Gets the example_block_eas of this FileProcedures.  # noqa: E501


        :return: The example_block_eas of this FileProcedures.  # noqa: E501
        :rtype: list[ProcedureBlock]
        """
        return self._example_block_eas

    @example_block_eas.setter
    def example_block_eas(self, example_block_eas):
        """Sets the example_block_eas of this FileProcedures.


        :param example_block_eas: The example_block_eas of this FileProcedures.  # noqa: E501
        :type: list[ProcedureBlock]
        """

        self._example_block_eas = example_block_eas

    @property
    def example_start_ea(self):
        """Gets the example_start_ea of this FileProcedures.  # noqa: E501


        :return: The example_start_ea of this FileProcedures.  # noqa: E501
        :rtype: str
        """
        return self._example_start_ea

    @example_start_ea.setter
    def example_start_ea(self, example_start_ea):
        """Sets the example_start_ea of this FileProcedures.


        :param example_start_ea: The example_start_ea of this FileProcedures.  # noqa: E501
        :type: str
        """

        self._example_start_ea = example_start_ea

    @property
    def example_end_ea(self):
        """Gets the example_end_ea of this FileProcedures.  # noqa: E501


        :return: The example_end_ea of this FileProcedures.  # noqa: E501
        :rtype: str
        """
        return self._example_end_ea

    @example_end_ea.setter
    def example_end_ea(self, example_end_ea):
        """Sets the example_end_ea of this FileProcedures.


        :param example_end_ea: The example_end_ea of this FileProcedures.  # noqa: E501
        :type: str
        """

        self._example_end_ea = example_end_ea

    @property
    def is_library(self):
        """Gets the is_library of this FileProcedures.  # noqa: E501


        :return: The is_library of this FileProcedures.  # noqa: E501
        :rtype: bool
        """
        return self._is_library

    @is_library.setter
    def is_library(self, is_library):
        """Sets the is_library of this FileProcedures.


        :param is_library: The is_library of this FileProcedures.  # noqa: E501
        :type: bool
        """

        self._is_library = is_library

    @property
    def block_counts(self):
        """Gets the block_counts of this FileProcedures.  # noqa: E501


        :return: The block_counts of this FileProcedures.  # noqa: E501
        :rtype: list[int]
        """
        return self._block_counts

    @block_counts.setter
    def block_counts(self, block_counts):
        """Sets the block_counts of this FileProcedures.


        :param block_counts: The block_counts of this FileProcedures.  # noqa: E501
        :type: list[int]
        """

        self._block_counts = block_counts

    @property
    def instr_counts(self):
        """Gets the instr_counts of this FileProcedures.  # noqa: E501


        :return: The instr_counts of this FileProcedures.  # noqa: E501
        :rtype: list[int]
        """
        return self._instr_counts

    @instr_counts.setter
    def instr_counts(self, instr_counts):
        """Sets the instr_counts of this FileProcedures.


        :param instr_counts: The instr_counts of this FileProcedures.  # noqa: E501
        :type: list[int]
        """

        self._instr_counts = instr_counts

    @property
    def byte_counts(self):
        """Gets the byte_counts of this FileProcedures.  # noqa: E501


        :return: The byte_counts of this FileProcedures.  # noqa: E501
        :rtype: list[int]
        """
        return self._byte_counts

    @byte_counts.setter
    def byte_counts(self, byte_counts):
        """Sets the byte_counts of this FileProcedures.


        :param byte_counts: The byte_counts of this FileProcedures.  # noqa: E501
        :type: list[int]
        """

        self._byte_counts = byte_counts

    @property
    def occurrence_counts(self):
        """Gets the occurrence_counts of this FileProcedures.  # noqa: E501


        :return: The occurrence_counts of this FileProcedures.  # noqa: E501
        :rtype: int
        """
        return self._occurrence_counts

    @occurrence_counts.setter
    def occurrence_counts(self, occurrence_counts):
        """Sets the occurrence_counts of this FileProcedures.


        :param occurrence_counts: The occurrence_counts of this FileProcedures.  # noqa: E501
        :type: int
        """

        self._occurrence_counts = occurrence_counts

    @property
    def name_counts(self):
        """Gets the name_counts of this FileProcedures.  # noqa: E501


        :return: The name_counts of this FileProcedures.  # noqa: E501
        :rtype: int
        """
        return self._name_counts

    @name_counts.setter
    def name_counts(self, name_counts):
        """Sets the name_counts of this FileProcedures.


        :param name_counts: The name_counts of this FileProcedures.  # noqa: E501
        :type: int
        """

        self._name_counts = name_counts

    @property
    def procedure_names(self):
        """Gets the procedure_names of this FileProcedures.  # noqa: E501


        :return: The procedure_names of this FileProcedures.  # noqa: E501
        :rtype: list[str]
        """
        return self._procedure_names

    @procedure_names.setter
    def procedure_names(self, procedure_names):
        """Sets the procedure_names of this FileProcedures.


        :param procedure_names: The procedure_names of this FileProcedures.  # noqa: E501
        :type: list[str]
        """

        self._procedure_names = procedure_names

    @property
    def coverage(self):
        """Gets the coverage of this FileProcedures.  # noqa: E501


        :return: The coverage of this FileProcedures.  # noqa: E501
        :rtype: float
        """
        return self._coverage

    @coverage.setter
    def coverage(self, coverage):
        """Sets the coverage of this FileProcedures.


        :param coverage: The coverage of this FileProcedures.  # noqa: E501
        :type: float
        """

        self._coverage = coverage

    @property
    def signature_count(self):
        """Gets the signature_count of this FileProcedures.  # noqa: E501


        :return: The signature_count of this FileProcedures.  # noqa: E501
        :rtype: int
        """
        return self._signature_count

    @signature_count.setter
    def signature_count(self, signature_count):
        """Sets the signature_count of this FileProcedures.


        :param signature_count: The signature_count of this FileProcedures.  # noqa: E501
        :type: int
        """

        self._signature_count = signature_count

    @property
    def example_procedure_count(self):
        """Gets the example_procedure_count of this FileProcedures.  # noqa: E501


        :return: The example_procedure_count of this FileProcedures.  # noqa: E501
        :rtype: int
        """
        return self._example_procedure_count

    @example_procedure_count.setter
    def example_procedure_count(self, example_procedure_count):
        """Sets the example_procedure_count of this FileProcedures.


        :param example_procedure_count: The example_procedure_count of this FileProcedures.  # noqa: E501
        :type: int
        """

        self._example_procedure_count = example_procedure_count

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
        if issubclass(FileProcedures, dict):
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
        if not isinstance(other, FileProcedures):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
