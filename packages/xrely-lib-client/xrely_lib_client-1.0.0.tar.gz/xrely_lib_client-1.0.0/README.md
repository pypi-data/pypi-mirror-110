# xrely-lib-client
API Documentation for XRELY platform

- API version: 1.0.0
- Package version: 1.0.0
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import xrely_lib_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import xrely_lib_client
```

Run testcases
```sh
python -m unittest -v test_data_api
```


## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import xrely_lib_client
from xrely_lib_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xrely_lib_client.DataApi(xrely_lib_client.ApiClient(configuration))
body = xrely_lib_client.DataStoreRequest() # DataStoreRequest |  (optional)

try:
    # Delete data from your account bucket
    api_response = api_instance.data_store_delete(body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DataApi->data_store_delete: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://www.xrely.com/api/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DataApi* | [**data_store_delete**](docs/DataApi.md#data_store_delete) | **DELETE** /data/store | Delete data from your account bucket
*DataApi* | [**data_store_post**](docs/DataApi.md#data_store_post) | **POST** /data/store | Insert data to your account bucket
*SearchApi* | [**search_post**](docs/SearchApi.md#search_post) | **POST** /search | Provides relevant result for your query
*SearchApi* | [**search_suggestions_get**](docs/SearchApi.md#search_suggestions_get) | **GET** /search/suggestions | Get autocomplete phrase or keywords for your query


## Documentation For Models

 - [AggrigationField](docs/AggrigationField.md)
 - [ApiResponse](docs/ApiResponse.md)
 - [DataApiResponse](docs/DataApiResponse.md)
 - [DataMessage](docs/DataMessage.md)
 - [DataStoreRequest](docs/DataStoreRequest.md)
 - [DocStoreItem](docs/DocStoreItem.md)
 - [FilterField](docs/FilterField.md)
 - [MapObject](docs/MapObject.md)
 - [SearchRequest](docs/SearchRequest.md)


## Documentation For Authorization

 All endpoints do not require authorization.


## Author

contact@xrely.com

