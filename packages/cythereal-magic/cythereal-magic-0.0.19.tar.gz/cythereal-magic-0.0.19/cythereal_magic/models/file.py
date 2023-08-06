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

class File(object):
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
        'public': 'bool',
        'sha1': 'str',
        'md5': 'str',
        'sha256': 'str',
        'sha512': 'str',
        'filetype': 'str',
        'object_class': 'str',
        'filenames': 'list[str]',
        'create_time': 'datetime',
        'match_count': 'int',
        'upload_time': 'datetime',
        'upload_times': 'list[UploadTimesChild]',
        'children': 'AllOfFileChildren',
        'parents': 'list[str]',
        'owned': 'bool',
        'notes': 'AllOfFileNotes',
        'tags': 'list[str]',
        'status': 'str',
        'pipeline': 'AllOfFilePipeline',
        'campaign': 'AllOfFileCampaign',
        'matches': 'AllOfFileMatches',
        'av_names': 'list[str]',
        'scanner_count': 'int',
        'detection_count': 'int',
        'evasiveness': 'float',
        'scan_date': 'datetime',
        'token_list': 'list[str]',
        'threat': 'str',
        'labels': 'AllOfFileLabels',
        'unmapped': 'AllOfFileUnmapped',
        'category': 'str',
        'categories': 'AllOfFileCategories',
        'family': 'str',
        'families': 'AllOfFileFamilies',
        'avscan': 'AllOfFileAvscan',
        'indicators': 'list[FileIndicator]',
        'reputation': 'AllOfFileReputation',
        'yara': 'str',
        'procedures': 'list[FileProcedures]',
        'procedure_group': 'str',
        'unpacked_procedures': 'list[FileProcedures]',
        'genomics': 'dict(str, HashSchema)',
        'unpacked_genomics': 'dict(str, HashSchema)',
        'similarities': 'list[FileSimilarityObject]'
    }

    attribute_map = {
        'public': 'public',
        'sha1': 'sha1',
        'md5': 'md5',
        'sha256': 'sha256',
        'sha512': 'sha512',
        'filetype': 'filetype',
        'object_class': 'object_class',
        'filenames': 'filenames',
        'create_time': 'create_time',
        'match_count': 'match_count',
        'upload_time': 'upload_time',
        'upload_times': 'upload_times',
        'children': 'children',
        'parents': 'parents',
        'owned': 'owned',
        'notes': 'notes',
        'tags': 'tags',
        'status': 'status',
        'pipeline': 'pipeline',
        'campaign': 'campaign',
        'matches': 'matches',
        'av_names': 'av_names',
        'scanner_count': 'scanner_count',
        'detection_count': 'detection_count',
        'evasiveness': 'evasiveness',
        'scan_date': 'scan_date',
        'token_list': 'token_list',
        'threat': 'threat',
        'labels': 'labels',
        'unmapped': 'unmapped',
        'category': 'category',
        'categories': 'categories',
        'family': 'family',
        'families': 'families',
        'avscan': 'avscan',
        'indicators': 'indicators',
        'reputation': 'reputation',
        'yara': 'yara',
        'procedures': 'procedures',
        'procedure_group': 'procedure_group',
        'unpacked_procedures': 'unpacked_procedures',
        'genomics': 'genomics',
        'unpacked_genomics': 'unpacked_genomics',
        'similarities': 'similarities'
    }

    def __init__(self, public=None, sha1=None, md5=None, sha256=None, sha512=None, filetype=None, object_class=None, filenames=None, create_time=None, match_count=None, upload_time=None, upload_times=None, children=None, parents=None, owned=None, notes=None, tags=None, status=None, pipeline=None, campaign=None, matches=None, av_names=None, scanner_count=None, detection_count=None, evasiveness=None, scan_date=None, token_list=None, threat=None, labels=None, unmapped=None, category=None, categories=None, family=None, families=None, avscan=None, indicators=None, reputation=None, yara=None, procedures=None, procedure_group=None, unpacked_procedures=None, genomics=None, unpacked_genomics=None, similarities=None):  # noqa: E501
        """File - a model defined in Swagger"""  # noqa: E501
        self._public = None
        self._sha1 = None
        self._md5 = None
        self._sha256 = None
        self._sha512 = None
        self._filetype = None
        self._object_class = None
        self._filenames = None
        self._create_time = None
        self._match_count = None
        self._upload_time = None
        self._upload_times = None
        self._children = None
        self._parents = None
        self._owned = None
        self._notes = None
        self._tags = None
        self._status = None
        self._pipeline = None
        self._campaign = None
        self._matches = None
        self._av_names = None
        self._scanner_count = None
        self._detection_count = None
        self._evasiveness = None
        self._scan_date = None
        self._token_list = None
        self._threat = None
        self._labels = None
        self._unmapped = None
        self._category = None
        self._categories = None
        self._family = None
        self._families = None
        self._avscan = None
        self._indicators = None
        self._reputation = None
        self._yara = None
        self._procedures = None
        self._procedure_group = None
        self._unpacked_procedures = None
        self._genomics = None
        self._unpacked_genomics = None
        self._similarities = None
        self.discriminator = None
        if public is not None:
            self.public = public
        if sha1 is not None:
            self.sha1 = sha1
        if md5 is not None:
            self.md5 = md5
        if sha256 is not None:
            self.sha256 = sha256
        if sha512 is not None:
            self.sha512 = sha512
        if filetype is not None:
            self.filetype = filetype
        if object_class is not None:
            self.object_class = object_class
        if filenames is not None:
            self.filenames = filenames
        if create_time is not None:
            self.create_time = create_time
        if match_count is not None:
            self.match_count = match_count
        if upload_time is not None:
            self.upload_time = upload_time
        if upload_times is not None:
            self.upload_times = upload_times
        if children is not None:
            self.children = children
        if parents is not None:
            self.parents = parents
        if owned is not None:
            self.owned = owned
        if notes is not None:
            self.notes = notes
        if tags is not None:
            self.tags = tags
        if status is not None:
            self.status = status
        if pipeline is not None:
            self.pipeline = pipeline
        if campaign is not None:
            self.campaign = campaign
        if matches is not None:
            self.matches = matches
        if av_names is not None:
            self.av_names = av_names
        if scanner_count is not None:
            self.scanner_count = scanner_count
        if detection_count is not None:
            self.detection_count = detection_count
        if evasiveness is not None:
            self.evasiveness = evasiveness
        if scan_date is not None:
            self.scan_date = scan_date
        if token_list is not None:
            self.token_list = token_list
        if threat is not None:
            self.threat = threat
        if labels is not None:
            self.labels = labels
        if unmapped is not None:
            self.unmapped = unmapped
        if category is not None:
            self.category = category
        if categories is not None:
            self.categories = categories
        if family is not None:
            self.family = family
        if families is not None:
            self.families = families
        if avscan is not None:
            self.avscan = avscan
        if indicators is not None:
            self.indicators = indicators
        if reputation is not None:
            self.reputation = reputation
        if yara is not None:
            self.yara = yara
        if procedures is not None:
            self.procedures = procedures
        if procedure_group is not None:
            self.procedure_group = procedure_group
        if unpacked_procedures is not None:
            self.unpacked_procedures = unpacked_procedures
        if genomics is not None:
            self.genomics = genomics
        if unpacked_genomics is not None:
            self.unpacked_genomics = unpacked_genomics
        if similarities is not None:
            self.similarities = similarities

    @property
    def public(self):
        """Gets the public of this File.  # noqa: E501


        :return: The public of this File.  # noqa: E501
        :rtype: bool
        """
        return self._public

    @public.setter
    def public(self, public):
        """Sets the public of this File.


        :param public: The public of this File.  # noqa: E501
        :type: bool
        """

        self._public = public

    @property
    def sha1(self):
        """Gets the sha1 of this File.  # noqa: E501


        :return: The sha1 of this File.  # noqa: E501
        :rtype: str
        """
        return self._sha1

    @sha1.setter
    def sha1(self, sha1):
        """Sets the sha1 of this File.


        :param sha1: The sha1 of this File.  # noqa: E501
        :type: str
        """

        self._sha1 = sha1

    @property
    def md5(self):
        """Gets the md5 of this File.  # noqa: E501


        :return: The md5 of this File.  # noqa: E501
        :rtype: str
        """
        return self._md5

    @md5.setter
    def md5(self, md5):
        """Sets the md5 of this File.


        :param md5: The md5 of this File.  # noqa: E501
        :type: str
        """

        self._md5 = md5

    @property
    def sha256(self):
        """Gets the sha256 of this File.  # noqa: E501


        :return: The sha256 of this File.  # noqa: E501
        :rtype: str
        """
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        """Sets the sha256 of this File.


        :param sha256: The sha256 of this File.  # noqa: E501
        :type: str
        """

        self._sha256 = sha256

    @property
    def sha512(self):
        """Gets the sha512 of this File.  # noqa: E501


        :return: The sha512 of this File.  # noqa: E501
        :rtype: str
        """
        return self._sha512

    @sha512.setter
    def sha512(self, sha512):
        """Sets the sha512 of this File.


        :param sha512: The sha512 of this File.  # noqa: E501
        :type: str
        """

        self._sha512 = sha512

    @property
    def filetype(self):
        """Gets the filetype of this File.  # noqa: E501


        :return: The filetype of this File.  # noqa: E501
        :rtype: str
        """
        return self._filetype

    @filetype.setter
    def filetype(self, filetype):
        """Sets the filetype of this File.


        :param filetype: The filetype of this File.  # noqa: E501
        :type: str
        """

        self._filetype = filetype

    @property
    def object_class(self):
        """Gets the object_class of this File.  # noqa: E501


        :return: The object_class of this File.  # noqa: E501
        :rtype: str
        """
        return self._object_class

    @object_class.setter
    def object_class(self, object_class):
        """Sets the object_class of this File.


        :param object_class: The object_class of this File.  # noqa: E501
        :type: str
        """

        self._object_class = object_class

    @property
    def filenames(self):
        """Gets the filenames of this File.  # noqa: E501


        :return: The filenames of this File.  # noqa: E501
        :rtype: list[str]
        """
        return self._filenames

    @filenames.setter
    def filenames(self, filenames):
        """Sets the filenames of this File.


        :param filenames: The filenames of this File.  # noqa: E501
        :type: list[str]
        """

        self._filenames = filenames

    @property
    def create_time(self):
        """Gets the create_time of this File.  # noqa: E501


        :return: The create_time of this File.  # noqa: E501
        :rtype: datetime
        """
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        """Sets the create_time of this File.


        :param create_time: The create_time of this File.  # noqa: E501
        :type: datetime
        """

        self._create_time = create_time

    @property
    def match_count(self):
        """Gets the match_count of this File.  # noqa: E501


        :return: The match_count of this File.  # noqa: E501
        :rtype: int
        """
        return self._match_count

    @match_count.setter
    def match_count(self, match_count):
        """Sets the match_count of this File.


        :param match_count: The match_count of this File.  # noqa: E501
        :type: int
        """

        self._match_count = match_count

    @property
    def upload_time(self):
        """Gets the upload_time of this File.  # noqa: E501


        :return: The upload_time of this File.  # noqa: E501
        :rtype: datetime
        """
        return self._upload_time

    @upload_time.setter
    def upload_time(self, upload_time):
        """Sets the upload_time of this File.


        :param upload_time: The upload_time of this File.  # noqa: E501
        :type: datetime
        """

        self._upload_time = upload_time

    @property
    def upload_times(self):
        """Gets the upload_times of this File.  # noqa: E501


        :return: The upload_times of this File.  # noqa: E501
        :rtype: list[UploadTimesChild]
        """
        return self._upload_times

    @upload_times.setter
    def upload_times(self, upload_times):
        """Sets the upload_times of this File.


        :param upload_times: The upload_times of this File.  # noqa: E501
        :type: list[UploadTimesChild]
        """

        self._upload_times = upload_times

    @property
    def children(self):
        """Gets the children of this File.  # noqa: E501


        :return: The children of this File.  # noqa: E501
        :rtype: AllOfFileChildren
        """
        return self._children

    @children.setter
    def children(self, children):
        """Sets the children of this File.


        :param children: The children of this File.  # noqa: E501
        :type: AllOfFileChildren
        """

        self._children = children

    @property
    def parents(self):
        """Gets the parents of this File.  # noqa: E501

        self referral field  # noqa: E501

        :return: The parents of this File.  # noqa: E501
        :rtype: list[str]
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this File.

        self referral field  # noqa: E501

        :param parents: The parents of this File.  # noqa: E501
        :type: list[str]
        """

        self._parents = parents

    @property
    def owned(self):
        """Gets the owned of this File.  # noqa: E501


        :return: The owned of this File.  # noqa: E501
        :rtype: bool
        """
        return self._owned

    @owned.setter
    def owned(self, owned):
        """Sets the owned of this File.


        :param owned: The owned of this File.  # noqa: E501
        :type: bool
        """

        self._owned = owned

    @property
    def notes(self):
        """Gets the notes of this File.  # noqa: E501


        :return: The notes of this File.  # noqa: E501
        :rtype: AllOfFileNotes
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this File.


        :param notes: The notes of this File.  # noqa: E501
        :type: AllOfFileNotes
        """

        self._notes = notes

    @property
    def tags(self):
        """Gets the tags of this File.  # noqa: E501

        self referral field  # noqa: E501

        :return: The tags of this File.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this File.

        self referral field  # noqa: E501

        :param tags: The tags of this File.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def status(self):
        """Gets the status of this File.  # noqa: E501

        self referral field  # noqa: E501

        :return: The status of this File.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this File.

        self referral field  # noqa: E501

        :param status: The status of this File.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def pipeline(self):
        """Gets the pipeline of this File.  # noqa: E501


        :return: The pipeline of this File.  # noqa: E501
        :rtype: AllOfFilePipeline
        """
        return self._pipeline

    @pipeline.setter
    def pipeline(self, pipeline):
        """Sets the pipeline of this File.


        :param pipeline: The pipeline of this File.  # noqa: E501
        :type: AllOfFilePipeline
        """

        self._pipeline = pipeline

    @property
    def campaign(self):
        """Gets the campaign of this File.  # noqa: E501


        :return: The campaign of this File.  # noqa: E501
        :rtype: AllOfFileCampaign
        """
        return self._campaign

    @campaign.setter
    def campaign(self, campaign):
        """Sets the campaign of this File.


        :param campaign: The campaign of this File.  # noqa: E501
        :type: AllOfFileCampaign
        """

        self._campaign = campaign

    @property
    def matches(self):
        """Gets the matches of this File.  # noqa: E501


        :return: The matches of this File.  # noqa: E501
        :rtype: AllOfFileMatches
        """
        return self._matches

    @matches.setter
    def matches(self, matches):
        """Sets the matches of this File.


        :param matches: The matches of this File.  # noqa: E501
        :type: AllOfFileMatches
        """

        self._matches = matches

    @property
    def av_names(self):
        """Gets the av_names of this File.  # noqa: E501


        :return: The av_names of this File.  # noqa: E501
        :rtype: list[str]
        """
        return self._av_names

    @av_names.setter
    def av_names(self, av_names):
        """Sets the av_names of this File.


        :param av_names: The av_names of this File.  # noqa: E501
        :type: list[str]
        """

        self._av_names = av_names

    @property
    def scanner_count(self):
        """Gets the scanner_count of this File.  # noqa: E501


        :return: The scanner_count of this File.  # noqa: E501
        :rtype: int
        """
        return self._scanner_count

    @scanner_count.setter
    def scanner_count(self, scanner_count):
        """Sets the scanner_count of this File.


        :param scanner_count: The scanner_count of this File.  # noqa: E501
        :type: int
        """

        self._scanner_count = scanner_count

    @property
    def detection_count(self):
        """Gets the detection_count of this File.  # noqa: E501


        :return: The detection_count of this File.  # noqa: E501
        :rtype: int
        """
        return self._detection_count

    @detection_count.setter
    def detection_count(self, detection_count):
        """Sets the detection_count of this File.


        :param detection_count: The detection_count of this File.  # noqa: E501
        :type: int
        """

        self._detection_count = detection_count

    @property
    def evasiveness(self):
        """Gets the evasiveness of this File.  # noqa: E501


        :return: The evasiveness of this File.  # noqa: E501
        :rtype: float
        """
        return self._evasiveness

    @evasiveness.setter
    def evasiveness(self, evasiveness):
        """Sets the evasiveness of this File.


        :param evasiveness: The evasiveness of this File.  # noqa: E501
        :type: float
        """

        self._evasiveness = evasiveness

    @property
    def scan_date(self):
        """Gets the scan_date of this File.  # noqa: E501


        :return: The scan_date of this File.  # noqa: E501
        :rtype: datetime
        """
        return self._scan_date

    @scan_date.setter
    def scan_date(self, scan_date):
        """Sets the scan_date of this File.


        :param scan_date: The scan_date of this File.  # noqa: E501
        :type: datetime
        """

        self._scan_date = scan_date

    @property
    def token_list(self):
        """Gets the token_list of this File.  # noqa: E501


        :return: The token_list of this File.  # noqa: E501
        :rtype: list[str]
        """
        return self._token_list

    @token_list.setter
    def token_list(self, token_list):
        """Sets the token_list of this File.


        :param token_list: The token_list of this File.  # noqa: E501
        :type: list[str]
        """

        self._token_list = token_list

    @property
    def threat(self):
        """Gets the threat of this File.  # noqa: E501


        :return: The threat of this File.  # noqa: E501
        :rtype: str
        """
        return self._threat

    @threat.setter
    def threat(self, threat):
        """Sets the threat of this File.


        :param threat: The threat of this File.  # noqa: E501
        :type: str
        """

        self._threat = threat

    @property
    def labels(self):
        """Gets the labels of this File.  # noqa: E501


        :return: The labels of this File.  # noqa: E501
        :rtype: AllOfFileLabels
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this File.


        :param labels: The labels of this File.  # noqa: E501
        :type: AllOfFileLabels
        """

        self._labels = labels

    @property
    def unmapped(self):
        """Gets the unmapped of this File.  # noqa: E501


        :return: The unmapped of this File.  # noqa: E501
        :rtype: AllOfFileUnmapped
        """
        return self._unmapped

    @unmapped.setter
    def unmapped(self, unmapped):
        """Sets the unmapped of this File.


        :param unmapped: The unmapped of this File.  # noqa: E501
        :type: AllOfFileUnmapped
        """

        self._unmapped = unmapped

    @property
    def category(self):
        """Gets the category of this File.  # noqa: E501


        :return: The category of this File.  # noqa: E501
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this File.


        :param category: The category of this File.  # noqa: E501
        :type: str
        """

        self._category = category

    @property
    def categories(self):
        """Gets the categories of this File.  # noqa: E501


        :return: The categories of this File.  # noqa: E501
        :rtype: AllOfFileCategories
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this File.


        :param categories: The categories of this File.  # noqa: E501
        :type: AllOfFileCategories
        """

        self._categories = categories

    @property
    def family(self):
        """Gets the family of this File.  # noqa: E501


        :return: The family of this File.  # noqa: E501
        :rtype: str
        """
        return self._family

    @family.setter
    def family(self, family):
        """Sets the family of this File.


        :param family: The family of this File.  # noqa: E501
        :type: str
        """

        self._family = family

    @property
    def families(self):
        """Gets the families of this File.  # noqa: E501


        :return: The families of this File.  # noqa: E501
        :rtype: AllOfFileFamilies
        """
        return self._families

    @families.setter
    def families(self, families):
        """Sets the families of this File.


        :param families: The families of this File.  # noqa: E501
        :type: AllOfFileFamilies
        """

        self._families = families

    @property
    def avscan(self):
        """Gets the avscan of this File.  # noqa: E501


        :return: The avscan of this File.  # noqa: E501
        :rtype: AllOfFileAvscan
        """
        return self._avscan

    @avscan.setter
    def avscan(self, avscan):
        """Sets the avscan of this File.


        :param avscan: The avscan of this File.  # noqa: E501
        :type: AllOfFileAvscan
        """

        self._avscan = avscan

    @property
    def indicators(self):
        """Gets the indicators of this File.  # noqa: E501


        :return: The indicators of this File.  # noqa: E501
        :rtype: list[FileIndicator]
        """
        return self._indicators

    @indicators.setter
    def indicators(self, indicators):
        """Sets the indicators of this File.


        :param indicators: The indicators of this File.  # noqa: E501
        :type: list[FileIndicator]
        """

        self._indicators = indicators

    @property
    def reputation(self):
        """Gets the reputation of this File.  # noqa: E501


        :return: The reputation of this File.  # noqa: E501
        :rtype: AllOfFileReputation
        """
        return self._reputation

    @reputation.setter
    def reputation(self, reputation):
        """Sets the reputation of this File.


        :param reputation: The reputation of this File.  # noqa: E501
        :type: AllOfFileReputation
        """

        self._reputation = reputation

    @property
    def yara(self):
        """Gets the yara of this File.  # noqa: E501


        :return: The yara of this File.  # noqa: E501
        :rtype: str
        """
        return self._yara

    @yara.setter
    def yara(self, yara):
        """Sets the yara of this File.


        :param yara: The yara of this File.  # noqa: E501
        :type: str
        """

        self._yara = yara

    @property
    def procedures(self):
        """Gets the procedures of this File.  # noqa: E501


        :return: The procedures of this File.  # noqa: E501
        :rtype: list[FileProcedures]
        """
        return self._procedures

    @procedures.setter
    def procedures(self, procedures):
        """Sets the procedures of this File.


        :param procedures: The procedures of this File.  # noqa: E501
        :type: list[FileProcedures]
        """

        self._procedures = procedures

    @property
    def procedure_group(self):
        """Gets the procedure_group of this File.  # noqa: E501


        :return: The procedure_group of this File.  # noqa: E501
        :rtype: str
        """
        return self._procedure_group

    @procedure_group.setter
    def procedure_group(self, procedure_group):
        """Sets the procedure_group of this File.


        :param procedure_group: The procedure_group of this File.  # noqa: E501
        :type: str
        """

        self._procedure_group = procedure_group

    @property
    def unpacked_procedures(self):
        """Gets the unpacked_procedures of this File.  # noqa: E501


        :return: The unpacked_procedures of this File.  # noqa: E501
        :rtype: list[FileProcedures]
        """
        return self._unpacked_procedures

    @unpacked_procedures.setter
    def unpacked_procedures(self, unpacked_procedures):
        """Sets the unpacked_procedures of this File.


        :param unpacked_procedures: The unpacked_procedures of this File.  # noqa: E501
        :type: list[FileProcedures]
        """

        self._unpacked_procedures = unpacked_procedures

    @property
    def genomics(self):
        """Gets the genomics of this File.  # noqa: E501


        :return: The genomics of this File.  # noqa: E501
        :rtype: dict(str, HashSchema)
        """
        return self._genomics

    @genomics.setter
    def genomics(self, genomics):
        """Sets the genomics of this File.


        :param genomics: The genomics of this File.  # noqa: E501
        :type: dict(str, HashSchema)
        """

        self._genomics = genomics

    @property
    def unpacked_genomics(self):
        """Gets the unpacked_genomics of this File.  # noqa: E501


        :return: The unpacked_genomics of this File.  # noqa: E501
        :rtype: dict(str, HashSchema)
        """
        return self._unpacked_genomics

    @unpacked_genomics.setter
    def unpacked_genomics(self, unpacked_genomics):
        """Sets the unpacked_genomics of this File.


        :param unpacked_genomics: The unpacked_genomics of this File.  # noqa: E501
        :type: dict(str, HashSchema)
        """

        self._unpacked_genomics = unpacked_genomics

    @property
    def similarities(self):
        """Gets the similarities of this File.  # noqa: E501


        :return: The similarities of this File.  # noqa: E501
        :rtype: list[FileSimilarityObject]
        """
        return self._similarities

    @similarities.setter
    def similarities(self, similarities):
        """Sets the similarities of this File.


        :param similarities: The similarities of this File.  # noqa: E501
        :type: list[FileSimilarityObject]
        """

        self._similarities = similarities

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
        if issubclass(File, dict):
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
        if not isinstance(other, File):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
