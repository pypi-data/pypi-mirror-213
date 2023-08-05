# coding: utf-8

"""
    MAGIC™ API

    --- # The API for accessing Unknown Cyber MAGIC products and services.  ---  ## Authentication  **(Head to our [/auth](../auth/swagger) api to register, login, or generate a token)**  Supported Authentication Schemes:   * HTTP Basic Authentication  * API-KEY in the `X-API-KEY` request header  * JWT token in the `Authorization:\"Bearer {token}\"` request header  ---  ## Content Negotiation    There are two ways to specify the content type of the response. In order of precedence:     * The **Accept** request header can be set with the desired mime type. The most specific version will prevail. i.e. *application/json* > *application/\\**.       *Accept:\"application/json\"*     * The **format** query parameter. (MUST be in lower case)       *?format=json*    Supported Formats:     | query parameter | Accept Header            |         |    |-----------------|--------------------------|---------|    | **json**        | application/json         | Default |    | **xml**         | application/xml          |         |    | **csv**         | text/csv                 |         |    | **txt**         | text/plain               |         |  --- ## Requests  Supported HTTP Methods:   * **GET**  * **POST**  * **PATCH**  * **DELETE**  * **HEAD**  * **OPTIONS**  Every request supports the following query parameters:   * **explain** - (bool) - Returns a detailed explanation of what the endpoint does, as well as potential query parameters that can be used to customize the results    * **download** - (bool) - If set to a truthy value, acts as setting the 'Content-Disposition' header to *\"attachment;\"* and will download the response as a file.   * **filename** - (str) - The filename to use for a downloaded file. Ignored if no file is being downloaded.        * **format** - (str) - Used in a similar manner to the *Accept* Header. Use this to specify which format you want the response returned in. Defaults to *application/json*. Current acceptable values are:      * **json** - (application/json)     * **xml** - (application/xml)     * **csv** - (text/csv)     * **txt** - (text/plain)         * Custom type that returns a description of usage of the endpoint   * **no_links** - (bool) - If set to a truthy value, links will be disabled from the response   * **uri** - (bool) - If set to a truthy value, id lists will be returned as uris instead of id strings.  ---  ## GET Conventions ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **read_mask** - A list of values (keys) to return for the resource or each resource within the list     * Comma separated string of variables     * Leaving this field blank will return the default values.     * Setting this value equal to **`*`** will include **ALL** possible keys.     * Traversal is allowed with the **`.`** operator.     * There are three special keys that can be used with all endponts         * **`*`** - This will return all possible values available         * **`_self`** - This will include the resources uri         * **`_default`** - This will include all default values (Those given with an empty read_mask)           * This would typically be used in conjunction with other 'non-default' fields       * Ex:         * `_default,family,category,_self`    * **dynamic_mask** - A list of dynamically generated values to return about the resource or each resource within the list     * Comma separated string of variables     * Operates the same as read_mask, but each variable will incur a much greater time cost.     * *May* cause timeouts     * Leaving this field blank or empty will return no dynamic variables.    * **expand_mask** - A list of relational variables to *expand* upon and return more than just the ids     * Comma separated string of variables     * Leaving this field blank will cause all relational data to be returned as a list of ids     * Ex:         * The `children` field for a file may return a list of ids normally, but with `children` set in the           `expand_mask`, it can return a list of child File objects with greater details.  ---  ## POST Conventions  This will create a new resource.  The resource data shall be provided in the request body.  The response will be either a 200 or 201, along with a uri to the newly created resource in the `Location` header.  In the case of a long running job, or reprocess, the response will be a 202 along with a **job_id** and it's corresponding **job_uri** that can be used in the */jobs/* endpoint to see the updated status  ---  ## PATCH Conventions   * The update data shall be provided in the request body.  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**    * **update_mask** - A list of values to update with this request.     * Comma separated string of variables     * This is required to be set for any and all **PATCH** requests to be processed.     * ONLY the specified variables in the update_mask will be updated regardless of the data in the request body.     * An empty or missing *update_mask* **WILL** result in a 400 Bad Request response  ---  ## DELETE Conventions  A successful response will return 204 No Content  ### Possible query parameters:   * **force** - Forces the deletion to go through     * This is required to be set as a truthy value for any and all **DELETE** requests to be processed.     * Not specifying this on a DELETE request (without *explain* set) **WILL** return a 400 Bad Request response   ---  ## *bulk* endpoints  **Bulk** endpoints are the ones that follow the  '*/<resource\\>/bulk/*' convention. They operate in the same fashion as the single resource endpoints ('*/<resource\\>/<resource_id\\>/*') except they can process multiple resources on a single call.  They **MUST** be a **POST** request along with the accompanying request body parameter to work:    * **ids** - A list of ids to operate on (For **GET**, **PATCH**, and **DELETE** bulk requests)   * **resources** - A list of resources to operate on (For **POST** bulk requests)  ### Possible query parameters:   **(Check each endpoint description, or use *explain*, for a list of available actions)**    * **action** - This is a string and can only be one of four values:      * **GET** - Returns a list of the resources, in the same order as provided in the request body.      * **POST** - Acts the same as a post on the pluralized resource endpoint.         * Instead of an **ids** request body parameter being provided in the request body, a **resources** list of new resources must be provided.      * **PATCH** - Acts the same as a patch on a single resource.          * Follows the same **PATCH** conventions from above*      * **DELETE** - Acts the same as a delete on a single resource.          * Follows the same **DELETE** conventions from above*    * **strict** - Causes the bulk endpoint to fail if a single provided id fails     * Boolean     * If set to True, the bulk call will ONLY operate if it is successful on ALL requested resources.     * If even a single resource is non-existent/forbidden, the call will fail and no side effects will take place.  ---  ## Pagination:  Pagination can be done in combination with sorting and filtering on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Pagination query paramters:        * **page_size** - The number of results to return (default: 50)   * **page_count** - The page used in pagination (default: 1)   * **skip_count** - A specified number of values to skip before collecting values (default: 0)  ---  ## Sorting:  Sorting can be done in combination with filtering and pagination on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Sorting query parameter:   **(Check each endpoint description, or use *explain*, for a list of available sorters)**    * **order_by** - A list of variables to sort the query on     * Comma separated string of variables     * Regex Pattern - `^(-?[\\w]+,?)*$`     * Variables are sorted in ascending order by default     * Prepend the variable with a `-` to change it to descending order     * Multiple sorters can be specified, with precedence matching the order of the parameter     * Ex:         * `-object_class,create_time`  ---  ## Filtering:  Filtering can be done in combination with pagination and sorting on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)  ### Filters query parameter:   **(Check each endpoint description, or use *explain*, for a list of available filters)**    * **filters** - A string of filters used to narrow down the query results.     * Semi-colon separated string of variables     * Regex patterns:         * Single filter:             * `^\\ *(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)\\ *`              * `NOT variable__comparator(value)`          * Multiple Filters:             * `^{SINGLE_FILTER_REGEX}(\\ +(AND|OR|;)\\ +{SINGLE_FILTER_REGEX})*$`              * `NOT variable__comparator(value) AND NOT variable__comparator(value); variable__comparator(value)`      * Logical operator order of precedence:         * **AND**         * **OR**         * **;** **(Semi-colon separation denotes conjunction)**         * Example order of precedence:             * **exp1;exp2 AND exp3 OR exp4** is equivalent to **(exp1) AND ((exp2 AND exp3) OR (exp4))**      * Available Comparators:         * **eq** - Equal         * **ne** - Not Equal         * **lt** - Less than         * **lte** - Less than or equal         * **gt** - Greater than         * **gte** - Greater than or equal         * **in** - In (for list values)         * **nin** - Not In (for list values)         * **regex** - Regular Expression Match         * **iregex** - Case Insensitive Regular Expression Match      * The format for **in** and **nin** which operate on arrays is:         * **[]** - The list of values must be enclosed within brackets.         * **,** - The value separtion token is a comma.         * **<variable\\>__<comp\\>([<value1\\>,<value2\\>])**      * Examples:         * `create_time__gte(2022-01-01T13:11:02);object_class__regex(binary.*)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01) AND NOT match_count__gt(10)`          * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01)`  ---  ## Responses  All responses **WILL** be of type `APIResponse` and contain the following fields:  * `success` | Boolean value indicating if the operation succeeded.  * `status` | Status code. Corresponds to the HTTP status code.   * `message` | A human readable message providing more details about the operation.  * `links` | A dictionary of `name`: `uri` links providing navigation and state-based actions on resources  * `errors` | Array of error objects. An error object contains the following properties:      * `reason` | Unique identifier for this error. Ex: \"FileNotFoundError\".      * `message`| Human readable error message.      * `parameter`| The parameter (if any) that caused the issue.  Successful operations **MUST** return a `SuccessResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal True  * `resource` | Properties containing the response object.     * (In the case of a single entity being returned)  **OR**  * `resources` | A list of response objects.     * (In the case of a list of entities being returned)  Failed Operations **MUST** return an `ErrorResponse`, which extends `APIResponse` by adding:  * `success` | **MUST** equal False.  Common Failed Operations that you may hit on any of the endpoint operations:  * 400 - Bad Request - The request is malformed  * 401 - Unauthorized - All endpoints require authorization  * 403 - Forbidden - The endpoint (with the given parameters) is not available to you  * 404 - Not Found - The endpoint doesn't exist, or the resource being searched for doesn't exist  ---  ## Example Inputs  Here are some example inputs that can be used for testing the service:  * `binary_id`: **ff9790d7902fea4c910b182f6e0b00221a40d616**  * `proc_rva`: **0x1000**  * `search_query`: **ransomware**  ---   # noqa: E501

    OpenAPI spec version: 2.0.0 (v2)
    Contact: support@unknowncyber.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from cythereal_magic.api_client import ApiClient


class TagsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def bulk_tag_operation(self, color2, ids2, color, ids, **kwargs):  # noqa: E501
        """Lists information on a bulk selection of tags  # noqa: E501

           Lists information on a bulk selection of tags           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.bulk_tag_operation(color2, ids2, color, ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str color2: (required)
        :param list[str] ids2: (required)
        :param str color: (required)
        :param list[str] ids: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :param bool force: MUST be true for any `DELETE` method to take place
        :param bool strict: Used for bulk sets of resources. If true, every resource must pass validation in order for any to be operated on
        :param str action: Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.bulk_tag_operation_with_http_info(color2, ids2, color, ids, **kwargs)  # noqa: E501
        else:
            (data) = self.bulk_tag_operation_with_http_info(color2, ids2, color, ids, **kwargs)  # noqa: E501
            return data

    def bulk_tag_operation_with_http_info(self, color2, ids2, color, ids, **kwargs):  # noqa: E501
        """Lists information on a bulk selection of tags  # noqa: E501

           Lists information on a bulk selection of tags           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.bulk_tag_operation_with_http_info(color2, ids2, color, ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str color2: (required)
        :param list[str] ids2: (required)
        :param str color: (required)
        :param list[str] ids: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :param bool force: MUST be true for any `DELETE` method to take place
        :param bool strict: Used for bulk sets of resources. If true, every resource must pass validation in order for any to be operated on
        :param str action: Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['color2', 'ids2', 'color', 'ids', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'update_mask', 'force', 'strict', 'action', 'read_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method bulk_tag_operation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'color2' is set
        if ('color2' not in params or
                params['color2'] is None):
            raise ValueError("Missing the required parameter `color2` when calling `bulk_tag_operation`")  # noqa: E501
        # verify the required parameter 'ids2' is set
        if ('ids2' not in params or
                params['ids2'] is None):
            raise ValueError("Missing the required parameter `ids2` when calling `bulk_tag_operation`")  # noqa: E501
        # verify the required parameter 'color' is set
        if ('color' not in params or
                params['color'] is None):
            raise ValueError("Missing the required parameter `color` when calling `bulk_tag_operation`")  # noqa: E501
        # verify the required parameter 'ids' is set
        if ('ids' not in params or
                params['ids'] is None):
            raise ValueError("Missing the required parameter `ids` when calling `bulk_tag_operation`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501
        if 'strict' in params:
            query_params.append(('strict', params['strict']))  # noqa: E501
        if 'action' in params:
            query_params.append(('action', params['action']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'ids' in params:
            form_params.append(('ids', params['ids']))  # noqa: E501
            collection_formats['ids'] = 'multi'  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'ids' in params:
            form_params.append(('ids', params['ids']))  # noqa: E501
            collection_formats['ids'] = 'multi'  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/bulk/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTagList200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def bulk_tag_operation(self, color2, ids2, color, ids, **kwargs):  # noqa: E501
        """Lists information on a bulk selection of tags  # noqa: E501

           Lists information on a bulk selection of tags           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.bulk_tag_operation(color2, ids2, color, ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str color2: (required)
        :param list[str] ids2: (required)
        :param str color: (required)
        :param list[str] ids: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :param bool force: MUST be true for any `DELETE` method to take place
        :param bool strict: Used for bulk sets of resources. If true, every resource must pass validation in order for any to be operated on
        :param str action: Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.bulk_tag_operation_with_http_info(color2, ids2, color, ids, **kwargs)  # noqa: E501
        else:
            (data) = self.bulk_tag_operation_with_http_info(color2, ids2, color, ids, **kwargs)  # noqa: E501
            return data

    def bulk_tag_operation_with_http_info(self, color2, ids2, color, ids, **kwargs):  # noqa: E501
        """Lists information on a bulk selection of tags  # noqa: E501

           Lists information on a bulk selection of tags           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.bulk_tag_operation_with_http_info(color2, ids2, color, ids, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str color2: (required)
        :param list[str] ids2: (required)
        :param str color: (required)
        :param list[str] ids: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :param bool force: MUST be true for any `DELETE` method to take place
        :param bool strict: Used for bulk sets of resources. If true, every resource must pass validation in order for any to be operated on
        :param str action: Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['color2', 'ids2', 'color', 'ids', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'update_mask', 'force', 'strict', 'action', 'read_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method bulk_tag_operation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'color2' is set
        if ('color2' not in params or
                params['color2'] is None):
            raise ValueError("Missing the required parameter `color2` when calling `bulk_tag_operation`")  # noqa: E501
        # verify the required parameter 'ids2' is set
        if ('ids2' not in params or
                params['ids2'] is None):
            raise ValueError("Missing the required parameter `ids2` when calling `bulk_tag_operation`")  # noqa: E501
        # verify the required parameter 'color' is set
        if ('color' not in params or
                params['color'] is None):
            raise ValueError("Missing the required parameter `color` when calling `bulk_tag_operation`")  # noqa: E501
        # verify the required parameter 'ids' is set
        if ('ids' not in params or
                params['ids'] is None):
            raise ValueError("Missing the required parameter `ids` when calling `bulk_tag_operation`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501
        if 'strict' in params:
            query_params.append(('strict', params['strict']))  # noqa: E501
        if 'action' in params:
            query_params.append(('action', params['action']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'ids' in params:
            form_params.append(('ids', params['ids']))  # noqa: E501
            collection_formats['ids'] = 'multi'  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'ids' in params:
            form_params.append(('ids', params['ids']))  # noqa: E501
            collection_formats['ids'] = 'multi'  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/bulk/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTagList200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def bulk_tag_operation(self, body, **kwargs):  # noqa: E501
        """Lists information on a bulk selection of tags  # noqa: E501

           Lists information on a bulk selection of tags           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.bulk_tag_operation(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param BulkTagRequest body: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :param bool force: MUST be true for any `DELETE` method to take place
        :param bool strict: Used for bulk sets of resources. If true, every resource must pass validation in order for any to be operated on
        :param str action: Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.bulk_tag_operation_with_http_info(body, **kwargs)  # noqa: E501
        else:
            (data) = self.bulk_tag_operation_with_http_info(body, **kwargs)  # noqa: E501
            return data

    def bulk_tag_operation_with_http_info(self, body, **kwargs):  # noqa: E501
        """Lists information on a bulk selection of tags  # noqa: E501

           Lists information on a bulk selection of tags           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.bulk_tag_operation_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param BulkTagRequest body: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :param bool force: MUST be true for any `DELETE` method to take place
        :param bool strict: Used for bulk sets of resources. If true, every resource must pass validation in order for any to be operated on
        :param str action: Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'update_mask', 'force', 'strict', 'action', 'read_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method bulk_tag_operation" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `bulk_tag_operation`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501
        if 'strict' in params:
            query_params.append(('strict', params['strict']))  # noqa: E501
        if 'action' in params:
            query_params.append(('action', params['action']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'ids' in params:
            form_params.append(('ids', params['ids']))  # noqa: E501
            collection_formats['ids'] = 'multi'  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'ids' in params:
            form_params.append(('ids', params['ids']))  # noqa: E501
            collection_formats['ids'] = 'multi'  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/bulk/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTagList200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_tag(self, **kwargs):  # noqa: E501
        """Create a new Project for tagging files  # noqa: E501

           Create a new Project for tagging files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_tag(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name2:
        :param str color2:
        :param str name:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool dryrun: If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed)
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_tag_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.create_tag_with_http_info(**kwargs)  # noqa: E501
            return data

    def create_tag_with_http_info(self, **kwargs):  # noqa: E501
        """Create a new Project for tagging files  # noqa: E501

           Create a new Project for tagging files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_tag_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name2:
        :param str color2:
        :param str name:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool dryrun: If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed)
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name2', 'color2', 'name', 'color', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'dryrun']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_tag" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'dryrun' in params:
            query_params.append(('dryrun', params['dryrun']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_tag(self, **kwargs):  # noqa: E501
        """Create a new Project for tagging files  # noqa: E501

           Create a new Project for tagging files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_tag(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name2:
        :param str color2:
        :param str name:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool dryrun: If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed)
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_tag_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.create_tag_with_http_info(**kwargs)  # noqa: E501
            return data

    def create_tag_with_http_info(self, **kwargs):  # noqa: E501
        """Create a new Project for tagging files  # noqa: E501

           Create a new Project for tagging files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_tag_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name2:
        :param str color2:
        :param str name:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool dryrun: If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed)
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name2', 'color2', 'name', 'color', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'dryrun']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_tag" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'dryrun' in params:
            query_params.append(('dryrun', params['dryrun']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_tag(self, **kwargs):  # noqa: E501
        """Create a new Project for tagging files  # noqa: E501

           Create a new Project for tagging files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_tag(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TagRequest body:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool dryrun: If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed)
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_tag_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.create_tag_with_http_info(**kwargs)  # noqa: E501
            return data

    def create_tag_with_http_info(self, **kwargs):  # noqa: E501
        """Create a new Project for tagging files  # noqa: E501

           Create a new Project for tagging files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_tag_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param TagRequest body:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool dryrun: If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed)
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'dryrun']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_tag" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'dryrun' in params:
            query_params.append(('dryrun', params['dryrun']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_tag(self, id, **kwargs):  # noqa: E501
        """Deletes a tag  # noqa: E501

           Deletes a tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_tag(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool force: MUST be true for any `DELETE` method to take place
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_tag_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_tag_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def delete_tag_with_http_info(self, id, **kwargs):  # noqa: E501
        """Deletes a tag  # noqa: E501

           Deletes a tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_tag_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool force: MUST be true for any `DELETE` method to take place
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `delete_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/{id}/', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_tags(self, **kwargs):  # noqa: E501
        """Delete tags in your collection  # noqa: E501

           Delete all tags in your collection           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_tags(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param bool force: MUST be true for any `DELETE` method to take place
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_tags_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.delete_tags_with_http_info(**kwargs)  # noqa: E501
            return data

    def delete_tags_with_http_info(self, **kwargs):  # noqa: E501
        """Delete tags in your collection  # noqa: E501

           Delete all tags in your collection           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_tags_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param bool force: MUST be true for any `DELETE` method to take place
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['format', 'explain', 'download', 'filename', 'no_links', 'uri', 'page_count', 'page_size', 'skip_count', 'filters', 'order_by', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_tags" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'page_count' in params:
            query_params.append(('page_count', params['page_count']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'skip_count' in params:
            query_params.append(('skip_count', params['skip_count']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_tag(self, id, **kwargs):  # noqa: E501
        """Retrieves detailed information on a single tag  # noqa: E501

           Retrieves detailed information on a single tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_tag(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTag200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_tag_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_tag_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def get_tag_with_http_info(self, id, **kwargs):  # noqa: E501
        """Retrieves detailed information on a single tag  # noqa: E501

           Retrieves detailed information on a single tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_tag_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTag200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'read_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `get_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/{id}/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTag200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_tagged_files(self, id, **kwargs):  # noqa: E501
        """Lists all files associated with this tag  # noqa: E501

           Lists all files associated with this tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_tagged_files(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :param str expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedFileList200EnvelopedIdList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_tagged_files_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.list_tagged_files_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def list_tagged_files_with_http_info(self, id, **kwargs):  # noqa: E501
        """Lists all files associated with this tag  # noqa: E501

           Lists all files associated with this tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_tagged_files_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :param str expand_mask: Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedFileList200EnvelopedIdList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'read_mask', 'expand_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_tagged_files" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `list_tagged_files`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501
        if 'expand_mask' in params:
            query_params.append(('expand_mask', params['expand_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/{id}/files/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedFileList200EnvelopedIdList200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_tags(self, **kwargs):  # noqa: E501
        """List all tags  # noqa: E501

           List all tags           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_tags(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_tags_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.list_tags_with_http_info(**kwargs)  # noqa: E501
            return data

    def list_tags_with_http_info(self, **kwargs):  # noqa: E501
        """List all tags  # noqa: E501

           List all tags           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_tags_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param str read_mask:  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$` 
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['format', 'explain', 'download', 'filename', 'no_links', 'uri', 'page_count', 'page_size', 'skip_count', 'filters', 'order_by', 'read_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_tags" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'page_count' in params:
            query_params.append(('page_count', params['page_count']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'skip_count' in params:
            query_params.append(('skip_count', params['skip_count']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'read_mask' in params:
            query_params.append(('read_mask', params['read_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTagList200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def remove_tags(self, id, **kwargs):  # noqa: E501
        """Removes a tag from all files  # noqa: E501

           Removes a tag from all files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_tags(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool force: MUST be true for any `DELETE` method to take place
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.remove_tags_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.remove_tags_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def remove_tags_with_http_info(self, id, **kwargs):  # noqa: E501
        """Removes a tag from all files  # noqa: E501

           Removes a tag from all files           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.remove_tags_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param bool force: MUST be true for any `DELETE` method to take place
        :return: ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'force']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method remove_tags" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `remove_tags`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'force' in params:
            query_params.append(('force', params['force']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/{id}/files/', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_tag(self, id, **kwargs):  # noqa: E501
        """Updates a tag  # noqa: E501

           Updates a tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tag(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str name2:
        :param str color2:
        :param str name:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTag200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_tag_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_tag_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def update_tag_with_http_info(self, id, **kwargs):  # noqa: E501
        """Updates a tag  # noqa: E501

           Updates a tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tag_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str name2:
        :param str color2:
        :param str name:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTag200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'name2', 'color2', 'name', 'color', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'update_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/{id}/', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTag200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_tag(self, id, **kwargs):  # noqa: E501
        """Updates a tag  # noqa: E501

           Updates a tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tag(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str name2:
        :param str color2:
        :param str name:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTag200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_tag_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_tag_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def update_tag_with_http_info(self, id, **kwargs):  # noqa: E501
        """Updates a tag  # noqa: E501

           Updates a tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tag_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param str name2:
        :param str color2:
        :param str name:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTag200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'name2', 'color2', 'name', 'color', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'update_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/{id}/', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTag200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_tag(self, id, **kwargs):  # noqa: E501
        """Updates a tag  # noqa: E501

           Updates a tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tag(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param PatchedTagRequest body:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTag200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_tag_with_http_info(id, **kwargs)  # noqa: E501
        else:
            (data) = self.update_tag_with_http_info(id, **kwargs)  # noqa: E501
            return data

    def update_tag_with_http_info(self, id, **kwargs):  # noqa: E501
        """Updates a tag  # noqa: E501

           Updates a tag           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tag_with_http_info(id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id: (required)
        :param PatchedTagRequest body:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTag200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id', 'body', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'update_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_tag" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'id' is set
        if ('id' not in params or
                params['id'] is None):
            raise ValueError("Missing the required parameter `id` when calling `update_tag`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'name' in params:
            form_params.append(('name', params['name']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/{id}/', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTag200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_tags(self, **kwargs):  # noqa: E501
        """Updates all tags in your collection  # noqa: E501

           Updates all tags in your collection           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tags(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str color2:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_tags_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.update_tags_with_http_info(**kwargs)  # noqa: E501
            return data

    def update_tags_with_http_info(self, **kwargs):  # noqa: E501
        """Updates all tags in your collection  # noqa: E501

           Updates all tags in your collection           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tags_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str color2:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['color2', 'color', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'page_count', 'page_size', 'skip_count', 'filters', 'order_by', 'update_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_tags" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'page_count' in params:
            query_params.append(('page_count', params['page_count']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'skip_count' in params:
            query_params.append(('skip_count', params['skip_count']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTagList200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_tags(self, **kwargs):  # noqa: E501
        """Updates all tags in your collection  # noqa: E501

           Updates all tags in your collection           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tags(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str color2:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_tags_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.update_tags_with_http_info(**kwargs)  # noqa: E501
            return data

    def update_tags_with_http_info(self, **kwargs):  # noqa: E501
        """Updates all tags in your collection  # noqa: E501

           Updates all tags in your collection           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tags_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str color2:
        :param str color:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['color2', 'color', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'page_count', 'page_size', 'skip_count', 'filters', 'order_by', 'update_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_tags" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'page_count' in params:
            query_params.append(('page_count', params['page_count']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'skip_count' in params:
            query_params.append(('skip_count', params['skip_count']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTagList200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_tags(self, **kwargs):  # noqa: E501
        """Updates all tags in your collection  # noqa: E501

           Updates all tags in your collection           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tags(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PatchedTagColorRequest body:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.update_tags_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.update_tags_with_http_info(**kwargs)  # noqa: E501
            return data

    def update_tags_with_http_info(self, **kwargs):  # noqa: E501
        """Updates all tags in your collection  # noqa: E501

           Updates all tags in your collection           # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_tags_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PatchedTagColorRequest body:
        :param str format: Format of the response from this endpoint
        :param bool explain: Shows the explain for this endpoint
        :param bool download: Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\")
        :param str filename: If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\")
        :param bool no_links: Removes the 'links' key
        :param bool uri: Use resource uri's in place of string ids
        :param int page_count:
        :param int page_size:
        :param int skip_count:
        :param str filters:  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`, 
        :param str order_by:  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$` 
        :param str update_mask: REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$`
        :return: EnvelopedTagList200ExplainResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'format', 'explain', 'download', 'filename', 'no_links', 'uri', 'page_count', 'page_size', 'skip_count', 'filters', 'order_by', 'update_mask']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_tags" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'format' in params:
            query_params.append(('format', params['format']))  # noqa: E501
        if 'explain' in params:
            query_params.append(('explain', params['explain']))  # noqa: E501
        if 'download' in params:
            query_params.append(('download', params['download']))  # noqa: E501
        if 'filename' in params:
            query_params.append(('filename', params['filename']))  # noqa: E501
        if 'no_links' in params:
            query_params.append(('no_links', params['no_links']))  # noqa: E501
        if 'uri' in params:
            query_params.append(('uri', params['uri']))  # noqa: E501
        if 'page_count' in params:
            query_params.append(('page_count', params['page_count']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('page_size', params['page_size']))  # noqa: E501
        if 'skip_count' in params:
            query_params.append(('skip_count', params['skip_count']))  # noqa: E501
        if 'filters' in params:
            query_params.append(('filters', params['filters']))  # noqa: E501
        if 'order_by' in params:
            query_params.append(('order_by', params['order_by']))  # noqa: E501
        if 'update_mask' in params:
            query_params.append(('update_mask', params['update_mask']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501
        if 'color' in params:
            form_params.append(('color', params['color']))  # noqa: E501

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml', 'text/csv', 'application/taxii+json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data', 'application/x-www-form-urlencoded', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Api Key Header Authentication', 'Api Key Query Authentication', 'Basic Authentication', 'JWT Access Token Authentication']  # noqa: E501

        return self.api_client.call_api(
            '/tags/', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='EnvelopedTagList200ExplainResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
