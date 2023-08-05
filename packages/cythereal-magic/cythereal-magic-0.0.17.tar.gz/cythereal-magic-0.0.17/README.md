# cythereal-magic

---
# The API for accessing Unknown Cyber MAGIC products and services.

---

## Authentication
 **(Head to our [/auth](../auth/swagger) api to register, login, or generate a token)**

Supported Authentication Schemes:

 * HTTP Basic Authentication
 * API-KEY in the `X-API-KEY` request header
 * JWT token in the `Authorization:"Bearer {token}"` request header

---

## Content Negotiation

  There are two ways to specify the content type of the response. In order of precedence:

   * The **Accept** request header can be set with the desired mime type. The most specific version will prevail. i.e. *application/json* > *application/\**.

     *Accept:"application/json"*

   * The **format** query parameter. (MUST be in lower case)

     *?format=json*

  Supported Formats:

   | query parameter | Accept Header            |         |
   |-----------------|--------------------------|---------|
   | **json**        | application/json         | Default |
   | **xml**         | application/xml          |         |
   | **csv**         | text/csv                 |         |
   | **txt**         | text/plain               |         |
   | **explain**     | application/explain+json | Custom type that returns a description of usage of the endpoint |

---
## Requests

Supported HTTP Methods:

 * **GET**
 * **POST**
 * **PATCH**
 * **DELETE**
 * **HEAD**
 * **OPTIONS**

Every request supports the following query parameters:

 * **explain** - (bool) - Returns a detailed explanation of what the endpoint does, as well as potential query parameters that can be used to customize the results

 * **download** - (bool) - If set to a truthy value, acts as setting the 'Content-Disposition' header to *"attachment;"* and will download the response as a file.

 * **filename** - (str) - The filename to use for a downloaded file. Ignored if no file is being downloaded.

 * **format** - (str) - Used in a similar manner to the *Accept* Header. Use this to specify which format you want the response returned in. Defaults to *application/json*. Current acceptable values are:

    * **json** - (application/json)
    * **xml** - (application/xml)
    * **csv** - (text/csv)
    * **txt** - (text/plain)
    * **explain** - (application/explain+json)
        * Custom type that returns a description of usage of the endpoint

 * **no_links** - (bool) - If set to a truthy value, links will be disabled from the response

 * **uri** - (bool) - If set to a truthy value, id lists will be returned as uris instead of id strings.

---

## GET Conventions
### Possible query parameters:
  **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**

  * **read_mask** - A list of values (keys) to return for the resource or each resource within the list
    * Comma separated string of variables
    * Leaving this field blank will return the default values.
    * Setting this value equal to **`*`** will include **ALL** possible keys.
    * Traversal is allowed with the **`.`** operator.
    * There are three special keys that can be used with all endponts
        * **`*`** - This will return all possible values available
        * **`_self`** - This will include the resources uri
        * **`_default`** - This will include all default values (Those given with an empty read_mask)
          * This would typically be used in conjunction with other 'non-default' fields
    * Ex:
        * `_default,family,category,_self`

  * **dynamic_mask** - A list of dynamically generated values to return about the resource or each resource within the list
    * Comma separated string of variables
    * Operates the same as read_mask, but each variable will incur a much greater time cost.
    * *May* cause timeouts
    * Leaving this field blank or empty will return no dynamic variables.

  * **expand_mask** - A list of relational variables to *expand* upon and return more than just the ids
    * Comma separated string of variables
    * Leaving this field blank will cause all relational data to be returned as a list of ids
    * Ex:
        * The `children` field for a file may return a list of ids normally, but with `children` set in the
          `expand_mask`, it can return a list of child File objects with greater details.

---

## POST Conventions

This will create a new resource.

The resource data shall be provided in the request body.

The response will be either a 200 or 201, along with a uri to the newly created resource in the `Location` header.

In the case of a long running job, or reprocess, the response will be a 202 along with a **job_id** and it's corresponding **job_uri** that can be used in the */jobs/* endpoint to see the updated status

---

## PATCH Conventions

 * The update data shall be provided in the request body.

### Possible query parameters:
  **(Check each endpoint description, or use *explain*, for a list of available values for each parameter)**

  * **update_mask** - A list of values to update with this request.
    * Comma separated string of variables
    * This is required to be set for any and all **PATCH** requests to be processed.
    * ONLY the specified variables in the update_mask will be updated regardless of the data in the request body.
    * An empty or missing *update_mask* **WILL** result in a 400 Bad Request response

---

## DELETE Conventions

A successful response will return 204 No Content

### Possible query parameters:
  * **force** - Forces the deletion to go through
    * This is required to be set as a truthy value for any and all **DELETE** requests to be processed.
    * Not specifying this on a DELETE request (without *explain* set) **WILL** return a 400 Bad Request response

---

## *bulk* endpoints

**Bulk** endpoints are the ones that follow the  '*/<resource\>/bulk/*' convention. They operate in the same fashion as the single resource endpoints ('*/<resource\>/<resource_id\>/*') except they can process multiple resources on a single call.

They **MUST** be a **POST** request along with the accompanying request body parameter to work:

  * **ids** - A list of ids to operate on (For **GET**, **PATCH**, and **DELETE** bulk requests)
  * **resources** - A list of resources to operate on (For **POST** bulk requests)

### Possible query parameters:
  **(Check each endpoint description, or use *explain*, for a list of available actions)**

  * **action** - This is a string and can only be one of four values:

    * **GET** - Returns a list of the resources, in the same order as provided in the request body.

    * **POST** - Acts the same as a post on the pluralized resource endpoint.
        * Instead of an **ids** request body parameter being provided in the request body, a **resources** list of new resources must be provided.

    * **PATCH** - Acts the same as a patch on a single resource.
        * Follows the same **PATCH** conventions from above*

    * **DELETE** - Acts the same as a delete on a single resource.
        * Follows the same **DELETE** conventions from above*

  * **strict** - Causes the bulk endpoint to fail if a single provided id fails
    * Boolean
    * If set to True, the bulk call will ONLY operate if it is successful on ALL requested resources.
    * If even a single resource is non-existent/forbidden, the call will fail and no side effects will take place.

---

## Pagination:

Pagination can be done in combination with sorting and filtering on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)

### Pagination query paramters:

  * **page_size** - The number of results to return (default: 50)
  * **page_count** - The page used in pagination (default: 1)
  * **skip_count** - A specified number of values to skip before collecting values (default: 0)

---

## Sorting:

Sorting can be done in combination with filtering and pagination on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)

### Sorting query parameter:
  **(Check each endpoint description, or use *explain*, for a list of available sorters)**

  * **order_by** - A list of variables to sort the query on
    * Comma separated string of variables
    * Regex Pattern - `^(-?[\w]+,?)*$`
    * Variables are sorted in ascending order by default
    * Prepend the variable with a `-` to change it to descending order
    * Multiple sorters can be specified, with precedence matching the order of the parameter
    * Ex:
        * `-object_class,create_time`

---

## Filtering:

Filtering can be done in combination with pagination and sorting on most endpoints that deal with lists (including **PATCH** and **DELETE** calls)

### Filters query parameter:
  **(Check each endpoint description, or use *explain*, for a list of available filters)**

  * **filters** - A string of filters used to narrow down the query results.
    * Semi-colon separated string of variables
    * Regex patterns:
        * Single filter:
            * `^\ *(NOT\ +)?[\w]+__[a-z]+\(.+\)\ *`

            * `NOT variable__comparator(value)`

        * Multiple Filters:
            * `^{SINGLE_FILTER_REGEX}(\ +(AND|OR|;)\ +{SINGLE_FILTER_REGEX})*$`

            * `NOT variable__comparator(value) AND NOT variable__comparator(value); variable__comparator(value)`

    * Logical operator order of precedence:
        * **AND**
        * **OR**
        * **;** **(Semi-colon separation denotes conjunction)**
        * Example order of precedence:
            * **exp1;exp2 AND exp3 OR exp4** is equivalent to **(exp1) AND ((exp2 AND exp3) OR (exp4))**

    * Available Comparators:
        * **eq** - Equal
        * **ne** - Not Equal
        * **lt** - Less than
        * **lte** - Less than or equal
        * **gt** - Greater than
        * **gte** - Greater than or equal
        * **in** - In (for list values)
        * **nin** - Not In (for list values)
        * **regex** - Regular Expression Match
        * **iregex** - Case Insensitive Regular Expression Match

    * The format for **in** and **nin** which operate on arrays is:
        * **[]** - The list of values must be enclosed within brackets.
        * **,** - The value separtion token is a comma.
        * **<variable\>__<comp\>([<value1\>,<value2\>])**

    * Examples:
        * `create_time__gte(2022-01-01T13:11:02);object_class__regex(binary.*)`

        * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01) AND NOT match_count__gt(10)`

        * `create_time__gte(2022-01-01) AND create_time__lt(2022-02-01)`

---

## Responses

All responses **WILL** be of type `APIResponse` and contain the following fields:

* `success` | Boolean value indicating if the operation succeeded.

* `status` | Status code. Corresponds to the HTTP status code.

* `message` | A human readable message providing more details about the operation.

* `links` | A dictionary of `name`: `uri` links providing navigation and state-based actions on resources

* `errors` | Array of error objects. An error object contains the following properties:

    * `reason` | Unique identifier for this error. Ex: "FileNotFoundError".

    * `message`| Human readable error message.

    * `parameter`| The parameter (if any) that caused the issue.

Successful operations **MUST** return a `SuccessResponse`, which extends `APIResponse` by adding:

* `success` | **MUST** equal True

* `resource` | Properties containing the response object.

   * (In the case of a single entity being returned)

**OR**

* `resources` | A list of response objects.

   * (In the case of a list of entities being returned)

Failed Operations **MUST** return an `ErrorResponse`, which extends `APIResponse` by adding:

* `success` | **MUST** equal False.

Common Failed Operations that you may hit on any of the endpoint operations:

* 400 - Bad Request - The request is malformed

* 401 - Unauthorized - All endpoints require authorization

* 403 - Forbidden - The endpoint (with the given parameters) is not available to you

* 404 - Not Found - The endpoint doesn't exist, or the resource being searched for doesn't exist

---

## Example Inputs

Here are some example inputs that can be used for testing the service:

* `binary_id`: **ff9790d7902fea4c910b182f6e0b00221a40d616**

* `proc_rva`: **0x1000**

* `search_query`: **ransomware**

---

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 2.0.0 (v2)
- Package version: 0.0.17
- Build package: io.swagger.codegen.v3.generators.python.PythonClientCodegen
For more information, please visit [https://unknowncyber.com](https://unknowncyber.com)

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install 'git+https://bitbucket.org/unknowncyber/magic-clients.git@v1#egg=cythereal_magic&subdirectory=clients/python'
```
(you may need to run `pip` with root permission: `sudo pip install 'git+https://bitbucket.org/unknowncyber/magic-clients.git@v1#egg=cythereal_magic&subdirectory=clients/python'`)

Then import the package:
```python
import cythereal_magic 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import cythereal_magic
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import cythereal_magic
from cythereal_magic.rest import ApiException
from pprint import pprint

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
dryrun = true # bool | If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed) (optional)

try:
    # Adds a publicly accessible file to your account
    api_response = api_instance.add_file(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, dryrun=dryrun)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->add_file: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
tag_id = 'tag_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Associate an existing tag with a file
    api_response = api_instance.add_file_tag(binary_id, tag_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->add_file_tag: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
payload_id = 'payload_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
force = true # bool | Forces a payload to be added, even if one already exists (optional)

try:
    # Manually add a payload connection to a file
    api_response = api_instance.add_payload(binary_id, payload_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, force=force)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->add_payload: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
ids2 = ['ids_example'] # list[str] | 
ids = ['ids_example'] # list[str] | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
page_count = 1 # int |  (optional) (default to 1)
page_size = 50 # int |  (optional) (default to 50)
skip_count = 0 # int |  (optional) (default to 0)
filters = 'filters_example' # str |  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`,  (optional)
order_by = 'order_by_example' # str |  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$`  (optional)
read_mask = 'read_mask_example' # str |  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$`  (optional)
expand_mask = 'expand_mask_example' # str | Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$` (optional)
dryrun = true # bool | If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed) (optional)
force = true # bool | MUST be true for any `DELETE` method to take place (optional)
dynamic_mask = 'dynamic_mask_example' # str | Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$` (optional)
action = 'action_example' # str | Used in bulk queries. Bulk queries are always POST, so 'action' allows the user to set the desired method (optional)

try:
    # Allows for actions to be carried out on bulk sets of files
    api_response = api_instance.bulk_file_operation(ids2, ids, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, page_count=page_count, page_size=page_size, skip_count=skip_count, filters=filters, order_by=order_by, read_mask=read_mask, expand_mask=expand_mask, dryrun=dryrun, force=force, dynamic_mask=dynamic_mask, action=action)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->bulk_file_operation: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
label2 = 'label_example' # str | 
source2 = 'source_example' # str | 
score2 = 56 # int | 
label = 'label_example' # str | 
source = 'source_example' # str | 
score = 56 # int | 
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Creates a new custom category label for a file
    api_response = api_instance.create_file_category(label2, source2, score2, label, source, score, binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->create_file_category: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
label2 = 'label_example' # str | 
source2 = 'source_example' # str | 
score2 = 56 # int | 
label = 'label_example' # str | 
source = 'source_example' # str | 
score = 56 # int | 
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Creates a new custom family label for a file
    api_response = api_instance.create_file_family(label2, source2, score2, label, source, score, binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->create_file_family: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
job = 'job_example' # str | The job to reprocess for this file
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
force = true # bool | Forces a job to be run, even if previously successful (optional)

try:
    # Send a file for reprocessing
    api_response = api_instance.create_file_job(binary_id, job, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, force=force)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->create_file_job: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
note2 = 'note_example' # str | 
note = 'note_example' # str | 
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
dryrun = true # bool | If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed) (optional)

try:
    # Attaches a note to a file
    api_response = api_instance.create_file_note(note2, note, binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, dryrun=dryrun)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->create_file_note: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
files2 = ['files_example'] # list[str] | 
name2 = 'name_example' # str | 
unpacked2 = true # bool | 
config2 = NULL # object | 
include_all2 = true # bool | 
max_signatures2 = 56 # int | 
files = ['files_example'] # list[str] | 
name = 'name_example' # str | 
unpacked = true # bool | 
config = NULL # object | 
include_all = true # bool | 
max_signatures = 56 # int | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
dryrun = true # bool | If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed) (optional)
strict = true # bool | Used for bulk sets of resources. If true, every resource must pass validation in order for any to be operated on (optional)

try:
    # Create Yara Rule based on multiple file hashes
    api_response = api_instance.create_files_yara(files2, name2, unpacked2, config2, include_all2, max_signatures2, files, name, unpacked, config, include_all, max_signatures, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, dryrun=dryrun, strict=strict)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->create_files_yara: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
note_id = 'note_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
force = true # bool | MUST be true for any `DELETE` method to take place (optional)

try:
    # Deletes a specified user note attached to a file
    api_response = api_instance.delete_file_note(binary_id, note_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, force=force)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->delete_file_note: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
force = true # bool | MUST be true for any `DELETE` method to take place (optional)

try:
    # Manually remove a payload connection from a file
    api_response = api_instance.delete_payload_relationship(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, force=force)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->delete_payload_relationship: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'format_example' # str |  (optional)
zipped = true # bool | If true, the returned download will be in an encrypted zip file (password=infected) (optional)

try:
    # Download file
    api_response = api_instance.download_file(binary_id, format=format, zipped=zipped)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->download_file: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
read_mask = 'read_mask_example' # str |  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$`  (optional)
expand_mask = 'expand_mask_example' # str | Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$` (optional)
dynamic_mask = 'dynamic_mask_example' # str | Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$` (optional)

try:
    # Retrieves information for a single file
    api_response = api_instance.get_file(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, read_mask=read_mask, expand_mask=expand_mask, dynamic_mask=dynamic_mask)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->get_file: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Retrieves a file's campaign information
    api_instance.get_file_campaign(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
except ApiException as e:
    print("Exception when calling FilesApi->get_file_campaign: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
note_id = 'note_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Retrieves a single note attached to a file
    api_response = api_instance.get_file_note(binary_id, note_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->get_file_note: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
verbose = true # bool | Whether to include all files that infer reputation (optional)

try:
    # Retrieves the reputation status of the file
    api_response = api_instance.get_file_reputation(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, verbose=verbose)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->get_file_reputation: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
config = 'relaxed' # str | The config of parameters to use when generating a yara rule (optional) (default to relaxed)
include_all = true # bool | Whether to include all procedures (optional)
unpacked = true # bool | Whether to use unpacked or original binaries (optional)
name = 'name_example' # str | The name of the yara rule (optional)

try:
    # Returns a yara rule for the given file
    api_response = api_instance.get_file_yara(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, config=config, include_all=include_all, unpacked=unpacked, name=name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->get_file_yara: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Retrieves a file's category labels
    api_response = api_instance.list_file_categories(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_categories: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Lists all files that were extracted as children
    api_response = api_instance.list_file_children(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_children: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Retrieves a file's family labels
    api_response = api_instance.list_file_families(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_families: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
page_count = 1 # int |  (optional) (default to 1)
page_size = 50 # int |  (optional) (default to 50)
skip_count = 0 # int |  (optional) (default to 0)
no_libs = true # bool | Whether to include library procedures (optional)

try:
    # Retrieves a file's genomics
    api_response = api_instance.list_file_genomics(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, page_count=page_count, page_size=page_size, skip_count=skip_count, no_libs=no_libs)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_genomics: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
malicious = true # bool | Whether to only show malicious indicators (optional) (default to true)

try:
    # Lists the Indicators of Compromise associated with a file
    api_response = api_instance.list_file_indicators(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, malicious=malicious)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_indicators: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Gets labels for a file
    api_response = api_instance.list_file_labels(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_labels: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
page_count = 1 # int |  (optional) (default to 1)
page_size = 50 # int |  (optional) (default to 50)
skip_count = 0 # int |  (optional) (default to 0)
read_mask = 'read_mask_example' # str |  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$`  (optional)
expand_mask = 'expand_mask_example' # str | Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$` (optional)
max_threshold = 3.4 # float | Only similarity matches at value equal or below max_threshold will be considered (optional)
min_threshold = 3.4 # float | Only similarity matches at value equal or above min_threshold will be considered (optional)

try:
    # Gets matches for a file
    api_response = api_instance.list_file_matches(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, page_count=page_count, page_size=page_size, skip_count=skip_count, read_mask=read_mask, expand_mask=expand_mask, max_threshold=max_threshold, min_threshold=min_threshold)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_matches: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Retrieves all user generated notes for file
    api_response = api_instance.list_file_notes(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_notes: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Retrieves a file's parent files
    api_response = api_instance.list_file_parents(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_parents: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
rva = 'rva_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Retrieves a procedure's genomics
    api_response = api_instance.list_file_procedure_genomics(binary_id, rva, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_procedure_genomics: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
page_count = 1 # int |  (optional) (default to 1)
page_size = 50 # int |  (optional) (default to 50)
skip_count = 0 # int |  (optional) (default to 0)
read_mask = 'read_mask_example' # str |  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$`  (optional)
unpacked = true # bool | Whether to use unpacked or original binaries (optional)

try:
    # Lists all procedures and their information for the given file
    api_response = api_instance.list_file_procedures(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, page_count=page_count, page_size=page_size, skip_count=skip_count, read_mask=read_mask, unpacked=unpacked)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_procedures: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
page_count = 1 # int |  (optional) (default to 1)
page_size = 50 # int |  (optional) (default to 50)
skip_count = 0 # int |  (optional) (default to 0)
max_threshold = 3.4 # float | Only similarity matches at value equal or below max_threshold will be considered (optional)
method = 'semantic_similarity' # str | Method to use to find similarities (optional) (default to semantic_similarity)
min_threshold = 3.4 # float | Only similarity matches at value equal or above min_threshold will be considered (optional)

try:
    # Retrieves similar file matches for the specified file
    api_response = api_instance.list_file_similarities(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, page_count=page_count, page_size=page_size, skip_count=skip_count, max_threshold=max_threshold, method=method, min_threshold=min_threshold)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_similarities: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # Gets strings for a file
    api_response = api_instance.list_file_strings(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_strings: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)

try:
    # List all user tags associated with a file
    api_response = api_instance.list_file_tags(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_tags: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
read_mask = 'read_mask_example' # str |  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$`  (optional)
expand_mask = 'expand_mask_example' # str | Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$` (optional)

try:
    api_response = api_instance.list_file_yara_matches(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, read_mask=read_mask, expand_mask=expand_mask)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_file_yara_matches: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
page_count = 1 # int |  (optional) (default to 1)
page_size = 50 # int |  (optional) (default to 50)
skip_count = 0 # int |  (optional) (default to 0)
filters = 'filters_example' # str |  Semi-colon separated string of filters. Each filter has a pattern of `(not)? <var>__<comp>(value)`   REGEX: `^(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\)(\\ +(AND|OR|;)\\ +(NOT\\ +)?[\\w]+__[a-z]+\\(.+\\))*$`,  (optional)
order_by = 'order_by_example' # str |  Comma separated string containing a list of keys to sort on. Prepend with a `-` for descending.   REGEX: `^(-?[\\w]+,?)*$`  (optional)
read_mask = 'read_mask_example' # str |  Comma separated string containing a list of keys to include in the response. `*` returns all keys.  REGEX: `^(([\\w]+,?)*|\\*)$`  (optional)
expand_mask = 'expand_mask_example' # str | Comma separated string containing a list of relation keys to `expand` and show the entire object inline.   REGEX: `^(([\\w]+,?)*|\\*)$` (optional)
dynamic_mask = 'dynamic_mask_example' # str | Comma separated string containing a list of dynamically created fields to return.   REGEX: `^(([\\w]+,?)*|\\*)$` (optional)

try:
    # List user files based on the parameters specified
    api_response = api_instance.list_files(format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, page_count=page_count, page_size=page_size, skip_count=skip_count, filters=filters, order_by=order_by, read_mask=read_mask, expand_mask=expand_mask, dynamic_mask=dynamic_mask)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->list_files: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
force = true # bool | MUST be true for any `DELETE` method to take place (optional)

try:
    # Removes a user's ownership from a single file
    api_response = api_instance.remove_file(binary_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, force=force)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->remove_file: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
tag_id = 'tag_id_example' # str | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
force = true # bool | MUST be true for any `DELETE` method to take place (optional)

try:
    # Remove an existing tag from a file
    api_response = api_instance.remove_file_tag(binary_id, tag_id, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, force=force)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->remove_file_tag: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
query = 'query_example' # str | Search query to look for
type = 'type_example' # str | Value type with which to search
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
page_count = 1 # int |  (optional) (default to 1)
page_size = 50 # int |  (optional) (default to 50)
skip_count = 0 # int |  (optional) (default to 0)

try:
    # Search for files based on given parameters
    api_response = api_instance.search_for_file(query, type, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, page_count=page_count, page_size=page_size, skip_count=skip_count)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->search_for_file: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
binary_id = 'binary_id_example' # str | 
public2 = true # bool |  (optional)
public = true # bool |  (optional)
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
update_mask = 'update_mask_example' # str | REQUIRED for `PATCH` methods. Comma separated string containing a list of keys to update based on the request body.  REGEX: `^(([\\w]+,?)*|\\*)$` (optional)

try:
    # Updates a single file
    api_response = api_instance.update_file(binary_id, public2=public2, public=public, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, update_mask=update_mask)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->update_file: %s\n" % e)

# Configure API key authorization: Api Key Header Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['X-API-KEY'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'
# Configure API key authorization: Api Key Query Authentication
configuration = cythereal_magic.Configuration()
configuration.api_key['key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['key'] = 'Bearer'# Configure HTTP basic authorization: Basic Authentication
configuration = cythereal_magic.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = cythereal_magic.FilesApi(cythereal_magic.ApiClient(configuration))
filedata2 = ['filedata_example'] # list[str] | 
password2 = 'password_example' # str | 
tags2 = ['tags_example'] # list[str] | 
notes2 = ['notes_example'] # list[str] | 
filedata = ['filedata_example'] # list[str] | 
password = 'password_example' # str | 
tags = ['tags_example'] # list[str] | 
notes = ['notes_example'] # list[str] | 
format = 'json' # str | Format of the response from this endpoint (optional) (default to json)
explain = true # bool | Shows the explain for this endpoint (optional)
download = true # bool | Determines whether to download the response.(Content-Disposition:\"attachment\" vs \"inline\") (optional)
filename = 'filename_example' # str | If download is True, this sets the name of the file. (Content-Disposition:\"attachment; filename=`filename`\") (optional)
no_links = true # bool | Removes the 'links' key (optional)
uri = true # bool | Use resource uri's in place of string ids (optional)
dryrun = true # bool | If True, don't cause any side effects.(Useful to check that an endpoint will work as constructed) (optional)
extract = true # bool | If true, all extracted files from an archive will be top level and the archive thrown away (optional)
recursive = true # bool | If true, all archives found in the upload will be stripped and thrown (optional)
retain_wrapper = true # bool | If true with extract, then the archive will not be thrown away (optional) (default to true)
skip_unpack = true # bool | If true, Unknown Cyber's default unpacker stage will be skipped (optional)

try:
    # Upload new files for processing
    api_response = api_instance.upload_file(filedata2, password2, tags2, notes2, filedata, password, tags, notes, format=format, explain=explain, download=download, filename=filename, no_links=no_links, uri=uri, dryrun=dryrun, extract=extract, recursive=recursive, retain_wrapper=retain_wrapper, skip_unpack=skip_unpack)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FilesApi->upload_file: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to *https://api:80/v2/*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*FilesApi* | [**add_file**](docs/FilesApi.md#add_file) | **POST** /files/{binary_id}/ | Adds a publicly accessible file to your account
*FilesApi* | [**add_file_tag**](docs/FilesApi.md#add_file_tag) | **POST** /files/{binary_id}/tags/{tag_id}/ | Associate an existing tag with a file
*FilesApi* | [**add_payload**](docs/FilesApi.md#add_payload) | **POST** /files/{binary_id}/payload/{payload_id}/ | Manually add a payload connection to a file
*FilesApi* | [**bulk_file_operation**](docs/FilesApi.md#bulk_file_operation) | **POST** /files/bulk/ | Allows for actions to be carried out on bulk sets of files
*FilesApi* | [**create_file_category**](docs/FilesApi.md#create_file_category) | **POST** /files/{binary_id}/categories/ | Creates a new custom category label for a file
*FilesApi* | [**create_file_family**](docs/FilesApi.md#create_file_family) | **POST** /files/{binary_id}/families/ | Creates a new custom family label for a file
*FilesApi* | [**create_file_job**](docs/FilesApi.md#create_file_job) | **POST** /files/{binary_id}/jobs/ | Send a file for reprocessing
*FilesApi* | [**create_file_note**](docs/FilesApi.md#create_file_note) | **POST** /files/{binary_id}/notes/ | Attaches a note to a file
*FilesApi* | [**create_files_yara**](docs/FilesApi.md#create_files_yara) | **POST** /files/yara/ | Create Yara Rule based on multiple file hashes
*FilesApi* | [**delete_file_note**](docs/FilesApi.md#delete_file_note) | **DELETE** /files/{binary_id}/notes/{note_id}/ | Deletes a specified user note attached to a file
*FilesApi* | [**delete_payload_relationship**](docs/FilesApi.md#delete_payload_relationship) | **DELETE** /files/{binary_id}/payload/ | Manually remove a payload connection from a file
*FilesApi* | [**download_file**](docs/FilesApi.md#download_file) | **GET** /files/{binary_id}/download/ | Download file
*FilesApi* | [**get_file**](docs/FilesApi.md#get_file) | **GET** /files/{binary_id}/ | Retrieves information for a single file
*FilesApi* | [**get_file_campaign**](docs/FilesApi.md#get_file_campaign) | **GET** /files/{binary_id}/campaign/ | Retrieves a file&#x27;s campaign information
*FilesApi* | [**get_file_note**](docs/FilesApi.md#get_file_note) | **GET** /files/{binary_id}/notes/{note_id}/ | Retrieves a single note attached to a file
*FilesApi* | [**get_file_reputation**](docs/FilesApi.md#get_file_reputation) | **GET** /files/{binary_id}/reputation/ | Retrieves the reputation status of the file
*FilesApi* | [**get_file_yara**](docs/FilesApi.md#get_file_yara) | **GET** /files/{binary_id}/yara/ | Returns a yara rule for the given file
*FilesApi* | [**list_file_categories**](docs/FilesApi.md#list_file_categories) | **GET** /files/{binary_id}/categories/ | Retrieves a file&#x27;s category labels
*FilesApi* | [**list_file_children**](docs/FilesApi.md#list_file_children) | **GET** /files/{binary_id}/children/ | Lists all files that were extracted as children
*FilesApi* | [**list_file_families**](docs/FilesApi.md#list_file_families) | **GET** /files/{binary_id}/families/ | Retrieves a file&#x27;s family labels
*FilesApi* | [**list_file_genomics**](docs/FilesApi.md#list_file_genomics) | **GET** /files/{binary_id}/genomics/ | Retrieves a file&#x27;s genomics
*FilesApi* | [**list_file_indicators**](docs/FilesApi.md#list_file_indicators) | **GET** /files/{binary_id}/indicators/ | Lists the Indicators of Compromise associated with a file
*FilesApi* | [**list_file_labels**](docs/FilesApi.md#list_file_labels) | **GET** /files/{binary_id}/labels/ | Gets labels for a file
*FilesApi* | [**list_file_matches**](docs/FilesApi.md#list_file_matches) | **GET** /files/{binary_id}/matches/ | Gets matches for a file
*FilesApi* | [**list_file_notes**](docs/FilesApi.md#list_file_notes) | **GET** /files/{binary_id}/notes/ | Retrieves all user generated notes for file
*FilesApi* | [**list_file_parents**](docs/FilesApi.md#list_file_parents) | **GET** /files/{binary_id}/parents/ | Retrieves a file&#x27;s parent files
*FilesApi* | [**list_file_procedure_genomics**](docs/FilesApi.md#list_file_procedure_genomics) | **GET** /files/{binary_id}/genomics/{rva}/ | Retrieves a procedure&#x27;s genomics
*FilesApi* | [**list_file_procedures**](docs/FilesApi.md#list_file_procedures) | **GET** /files/{binary_id}/procedures/ | Lists all procedures and their information for the given file
*FilesApi* | [**list_file_similarities**](docs/FilesApi.md#list_file_similarities) | **GET** /files/{binary_id}/similarities/ | Retrieves similar file matches for the specified file
*FilesApi* | [**list_file_strings**](docs/FilesApi.md#list_file_strings) | **GET** /files/{binary_id}/strings/ | Gets strings for a file
*FilesApi* | [**list_file_tags**](docs/FilesApi.md#list_file_tags) | **GET** /files/{binary_id}/tags/ | List all user tags associated with a file
*FilesApi* | [**list_file_yara_matches**](docs/FilesApi.md#list_file_yara_matches) | **GET** /files/{binary_id}/yara/matches/ | 
*FilesApi* | [**list_files**](docs/FilesApi.md#list_files) | **GET** /files/ | List user files based on the parameters specified
*FilesApi* | [**remove_file**](docs/FilesApi.md#remove_file) | **DELETE** /files/{binary_id}/ | Removes a user&#x27;s ownership from a single file
*FilesApi* | [**remove_file_tag**](docs/FilesApi.md#remove_file_tag) | **DELETE** /files/{binary_id}/tags/{tag_id}/ | Remove an existing tag from a file
*FilesApi* | [**search_for_file**](docs/FilesApi.md#search_for_file) | **GET** /files/search/ | Search for files based on given parameters
*FilesApi* | [**update_file**](docs/FilesApi.md#update_file) | **PATCH** /files/{binary_id}/ | Updates a single file
*FilesApi* | [**upload_file**](docs/FilesApi.md#upload_file) | **POST** /files/ | Upload new files for processing
*GenomicsApi* | [**compare_files**](docs/GenomicsApi.md#compare_files) | **GET** /genomics/compare/ | Takes in a list of files and sends back comparison results (slow)
*GroupsApi* | [**add_member**](docs/GroupsApi.md#add_member) | **POST** /groups/{id}/members/{member_id}/ | Adds the &#x60;member_id&#x60; user to the &#x60;id&#x60; group
*GroupsApi* | [**add_new_member**](docs/GroupsApi.md#add_new_member) | **POST** /groups/{id}/members/ | Adds the given user to this group
*GroupsApi* | [**bulk_group_operation**](docs/GroupsApi.md#bulk_group_operation) | **POST** /groups/bulk/ | Bulk operations on Group resources
*GroupsApi* | [**create_group**](docs/GroupsApi.md#create_group) | **POST** /groups/ | Create a new group
*GroupsApi* | [**delete_group**](docs/GroupsApi.md#delete_group) | **DELETE** /groups/{id}/ | Deletes a group
*GroupsApi* | [**get_group**](docs/GroupsApi.md#get_group) | **GET** /groups/{id}/ | Retrieves detailed information on a single group
*GroupsApi* | [**get_member**](docs/GroupsApi.md#get_member) | **GET** /groups/{id}/members/{member_id}/ | Returns the user with &#x60;member_id&#x60; with their &#x60;id&#x60; group settings
*GroupsApi* | [**group_login**](docs/GroupsApi.md#group_login) | **GET** /groups/{id}/login/ | Returns a jwt Token for this group
*GroupsApi* | [**group_logout**](docs/GroupsApi.md#group_logout) | **GET** /groups/logout/ | Converts the group jwt back into a single user jwt
*GroupsApi* | [**list_groups**](docs/GroupsApi.md#list_groups) | **GET** /groups/ | List all accessible groups
*GroupsApi* | [**list_members**](docs/GroupsApi.md#list_members) | **GET** /groups/{id}/members/ | List all members of a group
*GroupsApi* | [**remove_member**](docs/GroupsApi.md#remove_member) | **DELETE** /groups/{id}/members/{member_id}/ | Removes the &#x60;member_id&#x60; user from the &#x60;id&#x60; group
*GroupsApi* | [**update_group**](docs/GroupsApi.md#update_group) | **PATCH** /groups/{id}/ | Updates a group
*GroupsApi* | [**update_member**](docs/GroupsApi.md#update_member) | **PATCH** /groups/{id}/members/{member_id}/ | Updates the &#x60;member_id&#x60; user in the &#x60;id&#x60; group
*IndicatorsApi* | [**list_iocs**](docs/IndicatorsApi.md#list_iocs) | **GET** /indicators/ | Lists all indicators associated with a user account
*IndicatorsApi* | [**upload_ioc_file**](docs/IndicatorsApi.md#upload_ioc_file) | **POST** /indicators/files/ | Upload a text or csv file for IoC Extraction
*ProceduresApi* | [**add_procedure_tag**](docs/ProceduresApi.md#add_procedure_tag) | **POST** /procedures/{proc_hash}/tags/ | Adds a tag to a procedure
*ProceduresApi* | [**bulk_procedure_operation**](docs/ProceduresApi.md#bulk_procedure_operation) | **POST** /procedures/bulk/ | Get procedures in bulk
*ProceduresApi* | [**create_procedure_note**](docs/ProceduresApi.md#create_procedure_note) | **POST** /procedures/{proc_hash}/notes/ | Adds a note to a procedure
*ProceduresApi* | [**create_procedures_yara**](docs/ProceduresApi.md#create_procedures_yara) | **POST** /procedures/yara/ | Create Yara Rule based on given multiple procedures
*ProceduresApi* | [**delete_procedure_note**](docs/ProceduresApi.md#delete_procedure_note) | **DELETE** /procedures/{proc_hash}/notes/{note_id}/ | Deletes a procedure&#x27;s note
*ProceduresApi* | [**delete_procedure_tag**](docs/ProceduresApi.md#delete_procedure_tag) | **DELETE** /procedures/{proc_hash}/tags/{tag_id}/ | Deletes a procedure&#x27;s tag
*ProceduresApi* | [**get_procedure**](docs/ProceduresApi.md#get_procedure) | **GET** /procedures/{proc_hash}/ | Get a single procedure
*ProceduresApi* | [**list_procedure_files**](docs/ProceduresApi.md#list_procedure_files) | **GET** /procedures/{proc_hash}/files/ | Retrieves a procedure&#x27;s files
*ProceduresApi* | [**list_procedure_notes**](docs/ProceduresApi.md#list_procedure_notes) | **GET** /procedures/{proc_hash}/notes/ | Lists a procedure&#x27;s notes
*ProceduresApi* | [**list_procedure_similarities**](docs/ProceduresApi.md#list_procedure_similarities) | **GET** /procedures/{proc_hash}/similarities/ | Lists a procedure&#x27;s similarities
*ProceduresApi* | [**list_procedure_tags**](docs/ProceduresApi.md#list_procedure_tags) | **GET** /procedures/{proc_hash}/tags/ | Lists a procedure&#x27;s tags
*ProceduresApi* | [**list_procedures**](docs/ProceduresApi.md#list_procedures) | **GET** /procedures/ | Get all procedures
*ReportsApi* | [**get_archive_report**](docs/ReportsApi.md#get_archive_report) | **GET** /reports/{binary_id}/archive/ | Retrieves the report info of a container like file
*ReportsApi* | [**get_report_features**](docs/ReportsApi.md#get_report_features) | **GET** /reports/{binary_id}/features/ | Retrieves the genomic features of a file
*SearchApi* | [**count_search_results**](docs/SearchApi.md#count_search_results) | **GET** /search/count/ | Returns total count of results via search
*SearchApi* | [**search_files**](docs/SearchApi.md#search_files) | **GET** /search/ | Returns files found via search
*SupportApi* | [**report_bug**](docs/SupportApi.md#report_bug) | **POST** /support/bug/ | Allows users to report a bug within the system
*TagsApi* | [**bulk_tag_operation**](docs/TagsApi.md#bulk_tag_operation) | **POST** /tags/bulk/ | Lists information on a bulk selection of tags
*TagsApi* | [**create_tag**](docs/TagsApi.md#create_tag) | **POST** /tags/ | Create a new Project for tagging files
*TagsApi* | [**delete_tag**](docs/TagsApi.md#delete_tag) | **DELETE** /tags/{id}/ | Deletes a tag
*TagsApi* | [**delete_tags**](docs/TagsApi.md#delete_tags) | **DELETE** /tags/ | Delete tags in your collection
*TagsApi* | [**get_tag**](docs/TagsApi.md#get_tag) | **GET** /tags/{id}/ | Retrieves detailed information on a single tag
*TagsApi* | [**list_tagged_files**](docs/TagsApi.md#list_tagged_files) | **GET** /tags/{id}/files/ | Lists all files associated with this tag
*TagsApi* | [**list_tags**](docs/TagsApi.md#list_tags) | **GET** /tags/ | List all tags
*TagsApi* | [**remove_tags**](docs/TagsApi.md#remove_tags) | **DELETE** /tags/{id}/files/ | Removes a tag from all files
*TagsApi* | [**update_tag**](docs/TagsApi.md#update_tag) | **PATCH** /tags/{id}/ | Updates a tag
*TagsApi* | [**update_tags**](docs/TagsApi.md#update_tags) | **PATCH** /tags/ | Updates all tags in your collection
*UsersApi* | [**deactivate_account**](docs/UsersApi.md#deactivate_account) | **DELETE** /users/me/ | Deactivate your account
*UsersApi* | [**get_account**](docs/UsersApi.md#get_account) | **GET** /users/me/ | Retrieve your account information
*UsersApi* | [**get_my_group**](docs/UsersApi.md#get_my_group) | **GET** /users/me/groups/{id}/ | Retrieve info for a group
*UsersApi* | [**leave_my_group**](docs/UsersApi.md#leave_my_group) | **DELETE** /users/me/groups/{id}/ | Leave group
*UsersApi* | [**leave_my_groups**](docs/UsersApi.md#leave_my_groups) | **DELETE** /users/me/groups/ | Leave all groups
*UsersApi* | [**list_my_groups**](docs/UsersApi.md#list_my_groups) | **GET** /users/me/groups/ | Lists your groups
*UsersApi* | [**update_account**](docs/UsersApi.md#update_account) | **PATCH** /users/me/ | Update your account information
*YaraApi* | [**create_yara**](docs/YaraApi.md#create_yara) | **POST** /yara/ | Create Yara Rule based on specific file hashes
*YaraApi* | [**yara_procedure_matches**](docs/YaraApi.md#yara_procedure_matches) | **GET** /yara/{binary_id}/matches/ | 

## Documentation For Models

 - [AllOfDirectReputationReputation](docs/AllOfDirectReputationReputation.md)
 - [AllOfFileAvscan](docs/AllOfFileAvscan.md)
 - [AllOfFileCampaign](docs/AllOfFileCampaign.md)
 - [AllOfFileCategories](docs/AllOfFileCategories.md)
 - [AllOfFileChildAvscan](docs/AllOfFileChildAvscan.md)
 - [AllOfFileChildCampaign](docs/AllOfFileChildCampaign.md)
 - [AllOfFileChildCategories](docs/AllOfFileChildCategories.md)
 - [AllOfFileChildFamilies](docs/AllOfFileChildFamilies.md)
 - [AllOfFileChildLabels](docs/AllOfFileChildLabels.md)
 - [AllOfFileChildMatches](docs/AllOfFileChildMatches.md)
 - [AllOfFileChildNotes](docs/AllOfFileChildNotes.md)
 - [AllOfFileChildPipeline](docs/AllOfFileChildPipeline.md)
 - [AllOfFileChildReputation](docs/AllOfFileChildReputation.md)
 - [AllOfFileChildUnmapped](docs/AllOfFileChildUnmapped.md)
 - [AllOfFileChildren](docs/AllOfFileChildren.md)
 - [AllOfFileFamilies](docs/AllOfFileFamilies.md)
 - [AllOfFileLabels](docs/AllOfFileLabels.md)
 - [AllOfFileMatchResponseAvscan](docs/AllOfFileMatchResponseAvscan.md)
 - [AllOfFileMatchResponseCampaign](docs/AllOfFileMatchResponseCampaign.md)
 - [AllOfFileMatchResponseCategories](docs/AllOfFileMatchResponseCategories.md)
 - [AllOfFileMatchResponseChildren](docs/AllOfFileMatchResponseChildren.md)
 - [AllOfFileMatchResponseFamilies](docs/AllOfFileMatchResponseFamilies.md)
 - [AllOfFileMatchResponseLabels](docs/AllOfFileMatchResponseLabels.md)
 - [AllOfFileMatchResponseMatchType](docs/AllOfFileMatchResponseMatchType.md)
 - [AllOfFileMatchResponseMatches](docs/AllOfFileMatchResponseMatches.md)
 - [AllOfFileMatchResponseNotes](docs/AllOfFileMatchResponseNotes.md)
 - [AllOfFileMatchResponsePipeline](docs/AllOfFileMatchResponsePipeline.md)
 - [AllOfFileMatchResponseReputation](docs/AllOfFileMatchResponseReputation.md)
 - [AllOfFileMatchResponseUnmapped](docs/AllOfFileMatchResponseUnmapped.md)
 - [AllOfFileMatches](docs/AllOfFileMatches.md)
 - [AllOfFileNotes](docs/AllOfFileNotes.md)
 - [AllOfFilePipeline](docs/AllOfFilePipeline.md)
 - [AllOfFilePipelineDashboardCampaign](docs/AllOfFilePipelineDashboardCampaign.md)
 - [AllOfFilePipelineDashboardReport](docs/AllOfFilePipelineDashboardReport.md)
 - [AllOfFilePipelineIocHandler](docs/AllOfFilePipelineIocHandler.md)
 - [AllOfFilePipelineProcHashSignatures](docs/AllOfFilePipelineProcHashSignatures.md)
 - [AllOfFilePipelineSimilarityComputation](docs/AllOfFilePipelineSimilarityComputation.md)
 - [AllOfFilePipelineSrlJuice](docs/AllOfFilePipelineSrlJuice.md)
 - [AllOfFilePipelineSrlScanners](docs/AllOfFilePipelineSrlScanners.md)
 - [AllOfFilePipelineSrlUnpacker](docs/AllOfFilePipelineSrlUnpacker.md)
 - [AllOfFilePipelineVariantHashSignatures](docs/AllOfFilePipelineVariantHashSignatures.md)
 - [AllOfFilePipelineWebRequestHandler](docs/AllOfFilePipelineWebRequestHandler.md)
 - [AllOfFileReputation](docs/AllOfFileReputation.md)
 - [AllOfFileReputationInferredReputation](docs/AllOfFileReputationInferredReputation.md)
 - [AllOfFileReputationReputation](docs/AllOfFileReputationReputation.md)
 - [AllOfFileUnmapped](docs/AllOfFileUnmapped.md)
 - [AllOfGroupAdmins](docs/AllOfGroupAdmins.md)
 - [AllOfGroupMembers](docs/AllOfGroupMembers.md)
 - [AllOfGroupReducedResponseAdmins](docs/AllOfGroupReducedResponseAdmins.md)
 - [AllOfGroupReducedResponseMembers](docs/AllOfGroupReducedResponseMembers.md)
 - [AllOfInferredReputationCriteria](docs/AllOfInferredReputationCriteria.md)
 - [AllOfInferredReputationReputation](docs/AllOfInferredReputationReputation.md)
 - [AllOfMatchMatchType](docs/AllOfMatchMatchType.md)
 - [AllOfMatchSubtypeMatchSubtype](docs/AllOfMatchSubtypeMatchSubtype.md)
 - [AllOfYaraProcedureRequestCondition](docs/AllOfYaraProcedureRequestCondition.md)
 - [AllOfYaraRequestConfig](docs/AllOfYaraRequestConfig.md)
 - [AllowedParameters](docs/AllowedParameters.md)
 - [AvScanResult](docs/AvScanResult.md)
 - [BadRequestResponse](docs/BadRequestResponse.md)
 - [BlockEA](docs/BlockEA.md)
 - [BlockSchema](docs/BlockSchema.md)
 - [BulkGroupRequest](docs/BulkGroupRequest.md)
 - [BulkProcedureRequest](docs/BulkProcedureRequest.md)
 - [BulkProcedureResponse](docs/BulkProcedureResponse.md)
 - [BulkRequest](docs/BulkRequest.md)
 - [BulkTagRequest](docs/BulkTagRequest.md)
 - [ChildResponse](docs/ChildResponse.md)
 - [ChildResponseIdList](docs/ChildResponseIdList.md)
 - [ConditionEnum](docs/ConditionEnum.md)
 - [ConfigEnum](docs/ConfigEnum.md)
 - [CriteriaEnum](docs/CriteriaEnum.md)
 - [DirectReputation](docs/DirectReputation.md)
 - [EnvelopedBulkProcedureResponseList200](docs/EnvelopedBulkProcedureResponseList200.md)
 - [EnvelopedBulkProcedureResponseList200ExplainResponse](docs/EnvelopedBulkProcedureResponseList200ExplainResponse.md)
 - [EnvelopedEmpty201](docs/EnvelopedEmpty201.md)
 - [EnvelopedFile200](docs/EnvelopedFile200.md)
 - [EnvelopedFile200ExplainResponse](docs/EnvelopedFile200ExplainResponse.md)
 - [EnvelopedFileChildList200](docs/EnvelopedFileChildList200.md)
 - [EnvelopedFileGenomicsResponse200](docs/EnvelopedFileGenomicsResponse200.md)
 - [EnvelopedFileGenomicsResponse200ExplainResponse](docs/EnvelopedFileGenomicsResponse200ExplainResponse.md)
 - [EnvelopedFileIndicatorResponseList200](docs/EnvelopedFileIndicatorResponseList200.md)
 - [EnvelopedFileIndicatorResponseList200ExplainResponse](docs/EnvelopedFileIndicatorResponseList200ExplainResponse.md)
 - [EnvelopedFileLabelCreateResponse201](docs/EnvelopedFileLabelCreateResponse201.md)
 - [EnvelopedFileLabelsList200](docs/EnvelopedFileLabelsList200.md)
 - [EnvelopedFileLabelsList200ExplainResponse](docs/EnvelopedFileLabelsList200ExplainResponse.md)
 - [EnvelopedFileList200](docs/EnvelopedFileList200.md)
 - [EnvelopedFileList200EnvelopedFileChildList200ExplainResponse](docs/EnvelopedFileList200EnvelopedFileChildList200ExplainResponse.md)
 - [EnvelopedFileList200EnvelopedIdList200ExplainResponse](docs/EnvelopedFileList200EnvelopedIdList200ExplainResponse.md)
 - [EnvelopedFileList200ExplainResponse](docs/EnvelopedFileList200ExplainResponse.md)
 - [EnvelopedFileMatchResponseList200](docs/EnvelopedFileMatchResponseList200.md)
 - [EnvelopedFileMatchResponseList200EnvelopedIdList200ExplainResponse](docs/EnvelopedFileMatchResponseList200EnvelopedIdList200ExplainResponse.md)
 - [EnvelopedFileProcedureResponseList200](docs/EnvelopedFileProcedureResponseList200.md)
 - [EnvelopedFileProcedureResponseList200ExplainResponse](docs/EnvelopedFileProcedureResponseList200ExplainResponse.md)
 - [EnvelopedFileReputationResponse200](docs/EnvelopedFileReputationResponse200.md)
 - [EnvelopedFileReputationResponse200ExplainResponse](docs/EnvelopedFileReputationResponse200ExplainResponse.md)
 - [EnvelopedFileResponse200](docs/EnvelopedFileResponse200.md)
 - [EnvelopedFileResponse200ExplainResponse](docs/EnvelopedFileResponse200ExplainResponse.md)
 - [EnvelopedFileResponse201](docs/EnvelopedFileResponse201.md)
 - [EnvelopedFileResponseList200](docs/EnvelopedFileResponseList200.md)
 - [EnvelopedFileResponseList200ExplainResponse](docs/EnvelopedFileResponseList200ExplainResponse.md)
 - [EnvelopedFileSearchResponseList200](docs/EnvelopedFileSearchResponseList200.md)
 - [EnvelopedFileSearchResponseList200ExplainResponse](docs/EnvelopedFileSearchResponseList200ExplainResponse.md)
 - [EnvelopedFileSimilarityResponseList200](docs/EnvelopedFileSimilarityResponseList200.md)
 - [EnvelopedFileSimilarityResponseList200ExplainResponse](docs/EnvelopedFileSimilarityResponseList200ExplainResponse.md)
 - [EnvelopedFileStringsResponseList200](docs/EnvelopedFileStringsResponseList200.md)
 - [EnvelopedFileStringsResponseList200ExplainResponse](docs/EnvelopedFileStringsResponseList200ExplainResponse.md)
 - [EnvelopedFileUpdateResponse206](docs/EnvelopedFileUpdateResponse206.md)
 - [EnvelopedFileUploadResponseList200](docs/EnvelopedFileUploadResponseList200.md)
 - [EnvelopedFileUploadResponseList200ExplainResponse](docs/EnvelopedFileUploadResponseList200ExplainResponse.md)
 - [EnvelopedFileUploadResponseList201](docs/EnvelopedFileUploadResponseList201.md)
 - [EnvelopedGroup200](docs/EnvelopedGroup200.md)
 - [EnvelopedGroup200ExplainResponse](docs/EnvelopedGroup200ExplainResponse.md)
 - [EnvelopedGroupCreatedResponse201](docs/EnvelopedGroupCreatedResponse201.md)
 - [EnvelopedGroupJwtResponse200](docs/EnvelopedGroupJwtResponse200.md)
 - [EnvelopedGroupJwtResponse200ExplainResponse](docs/EnvelopedGroupJwtResponse200ExplainResponse.md)
 - [EnvelopedGroupList200](docs/EnvelopedGroupList200.md)
 - [EnvelopedGroupList200ExplainResponse](docs/EnvelopedGroupList200ExplainResponse.md)
 - [EnvelopedGroupReducedResponseList200](docs/EnvelopedGroupReducedResponseList200.md)
 - [EnvelopedGroupReducedResponseList200ExplainResponse](docs/EnvelopedGroupReducedResponseList200ExplainResponse.md)
 - [EnvelopedIdList200](docs/EnvelopedIdList200.md)
 - [EnvelopedIdList200ExplainResponse](docs/EnvelopedIdList200ExplainResponse.md)
 - [EnvelopedIdList201](docs/EnvelopedIdList201.md)
 - [EnvelopedIndicatorFileUploadResponse200](docs/EnvelopedIndicatorFileUploadResponse200.md)
 - [EnvelopedIndicatorFileUploadResponse200ExplainResponse](docs/EnvelopedIndicatorFileUploadResponse200ExplainResponse.md)
 - [EnvelopedIndicatorResponseList200](docs/EnvelopedIndicatorResponseList200.md)
 - [EnvelopedIndicatorResponseList200ExplainResponse](docs/EnvelopedIndicatorResponseList200ExplainResponse.md)
 - [EnvelopedJobResponse201](docs/EnvelopedJobResponse201.md)
 - [EnvelopedMapping200](docs/EnvelopedMapping200.md)
 - [EnvelopedMapping200ExplainResponse](docs/EnvelopedMapping200ExplainResponse.md)
 - [EnvelopedNamelessNoteList200](docs/EnvelopedNamelessNoteList200.md)
 - [EnvelopedNamelessNoteList200EnvelopedIdList200ExplainResponse](docs/EnvelopedNamelessNoteList200EnvelopedIdList200ExplainResponse.md)
 - [EnvelopedNote200](docs/EnvelopedNote200.md)
 - [EnvelopedNote200ExplainResponse](docs/EnvelopedNote200ExplainResponse.md)
 - [EnvelopedNote201](docs/EnvelopedNote201.md)
 - [EnvelopedNoteList200](docs/EnvelopedNoteList200.md)
 - [EnvelopedNoteList200ExplainResponse](docs/EnvelopedNoteList200ExplainResponse.md)
 - [EnvelopedPayloadCreateResponse201](docs/EnvelopedPayloadCreateResponse201.md)
 - [EnvelopedProcedureGroup200](docs/EnvelopedProcedureGroup200.md)
 - [EnvelopedProcedureGroup200ExplainResponse](docs/EnvelopedProcedureGroup200ExplainResponse.md)
 - [EnvelopedProcedureResponse200](docs/EnvelopedProcedureResponse200.md)
 - [EnvelopedProcedureResponse200ExplainResponse](docs/EnvelopedProcedureResponse200ExplainResponse.md)
 - [EnvelopedProcedureSimilarityResponse200](docs/EnvelopedProcedureSimilarityResponse200.md)
 - [EnvelopedProcedureSimilarityResponse200ExplainResponse](docs/EnvelopedProcedureSimilarityResponse200ExplainResponse.md)
 - [EnvelopedProcedureTagCreatedResponse201](docs/EnvelopedProcedureTagCreatedResponse201.md)
 - [EnvelopedSearchCountResponseList200](docs/EnvelopedSearchCountResponseList200.md)
 - [EnvelopedSearchCountResponseList200ExplainResponse](docs/EnvelopedSearchCountResponseList200ExplainResponse.md)
 - [EnvelopedSearchResponseList200](docs/EnvelopedSearchResponseList200.md)
 - [EnvelopedSearchResponseList200ExplainResponse](docs/EnvelopedSearchResponseList200ExplainResponse.md)
 - [EnvelopedTag200](docs/EnvelopedTag200.md)
 - [EnvelopedTag200ExplainResponse](docs/EnvelopedTag200ExplainResponse.md)
 - [EnvelopedTagCreatedResponse201](docs/EnvelopedTagCreatedResponse201.md)
 - [EnvelopedTagList200](docs/EnvelopedTagList200.md)
 - [EnvelopedTagList200EnvelopedIdList200ExplainResponse](docs/EnvelopedTagList200EnvelopedIdList200ExplainResponse.md)
 - [EnvelopedTagList200ExplainResponse](docs/EnvelopedTagList200ExplainResponse.md)
 - [EnvelopedUser200](docs/EnvelopedUser200.md)
 - [EnvelopedUser200ExplainResponse](docs/EnvelopedUser200ExplainResponse.md)
 - [EnvelopedUserId201](docs/EnvelopedUserId201.md)
 - [EnvelopedUserList200](docs/EnvelopedUserList200.md)
 - [EnvelopedUserList200ExplainResponse](docs/EnvelopedUserList200ExplainResponse.md)
 - [EnvelopedYara200](docs/EnvelopedYara200.md)
 - [EnvelopedYara200ExplainResponse](docs/EnvelopedYara200ExplainResponse.md)
 - [EnvelopedYaraProcedure200](docs/EnvelopedYaraProcedure200.md)
 - [EnvelopedYaraProcedure200ExplainResponse](docs/EnvelopedYaraProcedure200ExplainResponse.md)
 - [ErrorObject](docs/ErrorObject.md)
 - [ExplainObject](docs/ExplainObject.md)
 - [ExplainResponse](docs/ExplainResponse.md)
 - [ExtendedProcedureResponse](docs/ExtendedProcedureResponse.md)
 - [File](docs/File.md)
 - [FileAddLabelRequest](docs/FileAddLabelRequest.md)
 - [FileAvscan](docs/FileAvscan.md)
 - [FileCampaign](docs/FileCampaign.md)
 - [FileChild](docs/FileChild.md)
 - [FileGenomicsResponse](docs/FileGenomicsResponse.md)
 - [FileIndicator](docs/FileIndicator.md)
 - [FileIndicatorResponse](docs/FileIndicatorResponse.md)
 - [FileLabelCreateResponse](docs/FileLabelCreateResponse.md)
 - [FileLabels](docs/FileLabels.md)
 - [FileMatchResponse](docs/FileMatchResponse.md)
 - [FileMatchesIdList](docs/FileMatchesIdList.md)
 - [FileNote](docs/FileNote.md)
 - [FileNoteIdList](docs/FileNoteIdList.md)
 - [FilePipeline](docs/FilePipeline.md)
 - [FileProcedureResponse](docs/FileProcedureResponse.md)
 - [FileProcedures](docs/FileProcedures.md)
 - [FileReputation](docs/FileReputation.md)
 - [FileReputationResponse](docs/FileReputationResponse.md)
 - [FileResponse](docs/FileResponse.md)
 - [FileSearchResponse](docs/FileSearchResponse.md)
 - [FileSimilarityObject](docs/FileSimilarityObject.md)
 - [FileSimilarityResponse](docs/FileSimilarityResponse.md)
 - [FileStringsResponse](docs/FileStringsResponse.md)
 - [FileUpdateResponse](docs/FileUpdateResponse.md)
 - [FileUploadRequest](docs/FileUploadRequest.md)
 - [FileUploadResponse](docs/FileUploadResponse.md)
 - [Filter](docs/Filter.md)
 - [ForbiddenResponse](docs/ForbiddenResponse.md)
 - [Group](docs/Group.md)
 - [GroupCreatedResponse](docs/GroupCreatedResponse.md)
 - [GroupJwtResponse](docs/GroupJwtResponse.md)
 - [GroupReducedResponse](docs/GroupReducedResponse.md)
 - [GroupRequest](docs/GroupRequest.md)
 - [HashSchema](docs/HashSchema.md)
 - [IndicatorFileUploadResponse](docs/IndicatorFileUploadResponse.md)
 - [IndicatorResponse](docs/IndicatorResponse.md)
 - [InferredData](docs/InferredData.md)
 - [InferredReputation](docs/InferredReputation.md)
 - [InferredReputationEnum](docs/InferredReputationEnum.md)
 - [JobResponse](docs/JobResponse.md)
 - [LabelSchema](docs/LabelSchema.md)
 - [Mapping](docs/Mapping.md)
 - [Match](docs/Match.md)
 - [MatchSubtype](docs/MatchSubtype.md)
 - [MatchSubtypeEnum](docs/MatchSubtypeEnum.md)
 - [MatchTypeEnum](docs/MatchTypeEnum.md)
 - [MethodEnum](docs/MethodEnum.md)
 - [MiniUser](docs/MiniUser.md)
 - [MiniUserIdList](docs/MiniUserIdList.md)
 - [NamelessNote](docs/NamelessNote.md)
 - [NotFoundResponse](docs/NotFoundResponse.md)
 - [Note](docs/Note.md)
 - [NoteRequest](docs/NoteRequest.md)
 - [ParameterExplanation](docs/ParameterExplanation.md)
 - [PatchedFileUpdateRequest](docs/PatchedFileUpdateRequest.md)
 - [PatchedGroupUpdateRequest](docs/PatchedGroupUpdateRequest.md)
 - [PatchedMemberUpdateRequest](docs/PatchedMemberUpdateRequest.md)
 - [PatchedTagColorRequest](docs/PatchedTagColorRequest.md)
 - [PatchedTagRequest](docs/PatchedTagRequest.md)
 - [PatchedUserUpdateRequest](docs/PatchedUserUpdateRequest.md)
 - [PayloadCreateResponse](docs/PayloadCreateResponse.md)
 - [PipelineStatusEnum](docs/PipelineStatusEnum.md)
 - [ProcedureBlock](docs/ProcedureBlock.md)
 - [ProcedureGroup](docs/ProcedureGroup.md)
 - [ProcedureResponse](docs/ProcedureResponse.md)
 - [ProcedureSimilarityItem](docs/ProcedureSimilarityItem.md)
 - [ProcedureSimilarityResponse](docs/ProcedureSimilarityResponse.md)
 - [ProcedureTagCreatedResponse](docs/ProcedureTagCreatedResponse.md)
 - [RepData](docs/RepData.md)
 - [SearchCountResponse](docs/SearchCountResponse.md)
 - [SearchResponse](docs/SearchResponse.md)
 - [Tag](docs/Tag.md)
 - [TagCreatedResponse](docs/TagCreatedResponse.md)
 - [TagRequest](docs/TagRequest.md)
 - [TaggedItem](docs/TaggedItem.md)
 - [UnauthenticatedResponse](docs/UnauthenticatedResponse.md)
 - [UploadIocFileRequest](docs/UploadIocFileRequest.md)
 - [UploadTimesChild](docs/UploadTimesChild.md)
 - [User](docs/User.md)
 - [UserId](docs/UserId.md)
 - [UserIdRequest](docs/UserIdRequest.md)
 - [VersionEnum](docs/VersionEnum.md)
 - [Yara](docs/Yara.md)
 - [YaraProcedure](docs/YaraProcedure.md)
 - [YaraProcedureRequest](docs/YaraProcedureRequest.md)
 - [YaraRequest](docs/YaraRequest.md)

## Documentation For Authorization


## Api Key Header Authentication

- **Type**: API key
- **API key parameter name**: X-API-KEY
- **Location**: HTTP header

## Api Key Query Authentication

- **Type**: API key
- **API key parameter name**: key
- **Location**: URL query string

## Basic Authentication

- **Type**: HTTP basic authentication

## JWT Access Token Authentication



## Author

support@unknowncyber.com
