# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['OpenApiDriver']

package_data = \
{'': ['*']}

install_requires = \
['robotframework-datadriver>=1.6.1',
 'robotframework-openapi-libcore>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'robotframework-openapidriver',
    'version': '4.1.0',
    'description': 'A library for contract-testing OpenAPI / Swagger APIs.',
    'long_description': '---\n---\n\n# OpenApiDriver for Robot Framework®\n\nOpenApiDriver is an extension of the Robot Framework® DataDriver library that allows\nfor generation and execution of test cases based on the information in an OpenAPI\ndocument (also known as Swagger document).\nThis document explains how to use the OpenApiDriver library.\n\nFor more information about Robot Framework®, see http://robotframework.org.\n\nFor more information about the DataDriver library, see\nhttps://github.com/Snooz82/robotframework-datadriver.\n\n---\n\n> Note: OpenApiDriver is still under development so there are currently\nrestrictions / limitations that you may encounter when using this library to run\ntests against an API. See [Limitations](#limitations) for details.\n\n---\n\n## Installation\n\nIf you already have Python >= 3.8 with pip installed, you can simply run:\n\n`pip install --upgrade robotframework-openapidriver`\n\n---\n\n## OpenAPI (aka Swagger)\n\nThe OpenAPI Specification (OAS) defines a standard, language-agnostic interface\nto RESTful APIs, see https://swagger.io/specification/\n\nThe OpenApiDriver module implements a reader class that generates a test case for\neach path, method and response (i.e. every response for each endpoint) that is defined\nin an OpenAPI document, typically an openapi.json or openapi.yaml file.\n\n> Note: OpenApiDriver is designed for APIs based on the OAS v3\nThe library has not been tested for APIs based on the OAS v2.\n\n---\n\n## Getting started\n\nBefore trying to use OpenApiDriver to run automatic validations on the target API\nit\'s recommended to first ensure that the openapi document for the API is valid\nunder the OpenAPI Specification.\n\nThis can be done using the command line interface of a package that is installed as\na prerequisite for OpenApiDriver.\nBoth a local openapi.json or openapi.yaml file or one hosted by the API server\ncan be checked using the `prance validate <reference_to_file>` shell command:\n\n```shell\nprance validate --backend=openapi-spec-validator http://localhost:8000/openapi.json\nProcessing "http://localhost:8000/openapi.json"...\n -> Resolving external references.\nValidates OK as OpenAPI 3.0.2!\n\nprance validate --backend=openapi-spec-validator /tests/files/petstore_openapi.yaml\nProcessing "/tests/files/petstore_openapi.yaml"...\n -> Resolving external references.\nValidates OK as OpenAPI 3.0.2!\n```\n\nYou\'ll have to change the url or file reference to the location of the openapi\ndocument for your API.\n\n> Note: Although recursion is technically allowed under the OAS, tool support is limited\nand changing the OAS to not use recursion is recommended.\nOpenApiDriver has limited support for parsing OpenAPI documents with\nrecursion in them. See the `recursion_limit` and `recursion_default` parameters.\n\nIf the openapi document passes this validation, the next step is trying to do a test\nrun with a minimal test suite.\nThe example below can be used, with `source` and `origin` altered to fit your situation.\n\n``` robotframework\n*** Settings ***\nLibrary            OpenApiDriver\n...                    source=http://localhost:8000/openapi.json\n...                    origin=http://localhost:8000\nTest Template      Validate Using Test Endpoint Keyword\n\n*** Test Cases ***\nTest Endpoint for ${method} on ${path} where ${status_code} is expected\n\n*** Keywords ***\nValidate Using Test Endpoint Keyword\n    [Arguments]    ${path}    ${method}    ${status_code}\n    Test Endpoint\n    ...    path=${path}    method=${method}    status_code=${status_code}\n\n```\n\nRunning the above suite for the first time is likely to result in some\nerrors / failed tests.\nYou should look at the Robot Framework `log.html` to determine the reasons\nfor the failing tests.\nDepending on the reasons for the failures, different solutions are possible.\n\nDetails about the OpenApiDriver library parameters that you may need can be found\n[here](https://marketsquare.github.io/robotframework-openapidriver/openapidriver.html).\n\nThe OpenApiDriver also support handling of relations between resources within the scope\nof the API being validated as well as handling dependencies on resources outside the\nscope of the API. In addition there is support for handling restrictions on the values\nof parameters and properties.\n\nDetails about the `mappings_path` variable usage can be found\n[here](https://marketsquare.github.io/robotframework-openapi-libcore/advanced_use.html).\n\n---\n\n## Limitations\n\nThere are currently a number of limitations to supported API structures, supported\ndata types and properties. The following list details the most important ones:\n- Only JSON request and response bodies are supported.\n- No support for per-path authorization levels (only simple 401 / 403 validation).\n\n',
    'author': 'Robin Mackaij',
    'author_email': 'r.a.mackaij@gmail.com',
    'maintainer': 'Robin Mackaij',
    'maintainer_email': 'r.a.mackaij@gmail.com',
    'url': 'https://github.com/MarketSquare/robotframework-openapidriver',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
