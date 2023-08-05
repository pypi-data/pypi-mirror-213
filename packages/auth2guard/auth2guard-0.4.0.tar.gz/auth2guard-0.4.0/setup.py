# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['auth2guard']

package_data = \
{'': ['*']}

install_requires = \
['jwt>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'auth2guard',
    'version': '0.4.0',
    'description': 'OAuth 2.0 scope validator',
    'long_description': '```\n░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\n░░░░░░░  ░░░░░░░░░░░░░░░░░░░   ░░░░░░░░░░░░░░░░░░░░░░░░░░     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ░\n▒▒▒▒▒▒  ▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▒▒▒   ▒▒▒▒▒▒▒   ▒  ▒▒▒▒▒  ▒▒▒▒   ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   ▒\n▒▒▒▒▒  ▒▒   ▒▒▒▒▒   ▒▒   ▒    ▒  ▒   ▒▒▒▒▒▒  ▒▒▒▒▒   ▒  ▒▒▒▒▒▒▒▒▒▒▒   ▒▒   ▒▒▒▒   ▒▒▒▒▒  ▒    ▒▒▒▒▒▒   ▒\n▓▓▓▓   ▓▓▓   ▓▓▓▓   ▓▓   ▓▓▓   ▓▓▓     ▓▓▓▓▓▓▓▓▓   ▓▓▓   ▓▓▓▓▓▓▓▓▓▓   ▓▓   ▓▓   ▓▓   ▓▓▓   ▓▓▓▓▓   ▓   ▓\n▓▓▓       ▓   ▓▓▓   ▓▓   ▓▓▓   ▓▓▓   ▓▓  ▓▓▓▓▓   ▓▓▓▓▓   ▓▓▓      ▓   ▓▓   ▓   ▓▓▓   ▓▓▓   ▓▓▓▓  ▓▓▓   ▓\n▓▓   ▓▓▓▓▓▓▓   ▓▓   ▓▓   ▓▓▓   ▓ ▓  ▓▓▓   ▓▓   ▓▓▓▓▓▓▓▓   ▓▓▓▓  ▓▓▓   ▓▓   ▓   ▓▓▓   ▓▓▓   ▓▓▓▓  ▓▓▓   ▓\n█   █████████   ███      ████   ██  ███   █         ████      ███████      ███   █    █    █████   █   █\n████████████████████████████████████████████████████████████████████████████████████████████████████████\nBy: CenturyBoys\n```\n\nA simple route decorator JWT scope validator.\n\nThis project work with the follow frameworks:\n\n✅ [FastApi](https://fastapi.tiangolo.com/)\n\n✅ [aiohttp](https://docs.aiohttp.org/en/stable/)\n\n## Config\n\nConfiguration are exposed and can be set in any time including out of the use scope.\n\nObs: all configs are saved as singleton.\n\n### jwk\n\nThe jwk key to validate JWT can be bytes, str or dict. This config need to be set!\n\n### http_header_name_token\n\nIf your application use a custom header to send the authentication token you can use this param to indicate his name. By default, the value is \'Authorization\'\n\n### request_token_callback\n\nIf to extract the request token you need to perform some operation you can set a callback for it. Will receive the request as param and must return a str with token type and the token \'Basic XXX\'\n\n```python\nimport auth2guard\n\nclass Request:\n    def __init__(self, headers: dict):\n        self._headers = headers\n\n    @property\n    def headers(self) -> dict:\n        return self._headersclass\n    \nrequest = Request(headers={"x-token": f"Basic Akj817Hakn122i..."})\n\ndef request_token_callback(request: Request):\n        return request.headers.get("x-token")\n    \n    \nauth2guard.set_config(\n    jwk=\'{"p":"-7pCvLlzsNIRD7utbLZqB...\',\n    http_header_name_token="x-token",\n    request_token_callback=request_token_callback\n)\n```\n\n## Exceptions\n\nThe package raise exceptions for some cases se bellow.\n\nObs: By default, all exception are ValueError.\n\n### token_not_found\nError when token was not found. \n\nObs: The config `request_token_callback` can be the problem.\n\n### not_from_origin\nError when token was generated not by the giving JWK. \n\nObs: Validate the config jwk.\n\n### expired\nError when exp JWT param exceeded the time.\n\n### unauthorized\nError when the JWT has not all necessary scope to proceed.\n\n```python\nimport auth2guard\n\nclass MyException(Exception):\n    pass\n\nauth2guard.overwrite_exceptions(unauthorized=MyException)\n```\n\n## Validator\n\nCan be used as decorator and receive a list of scopes. The validator will operate AND validation or a OR validation with the token scope content. For the AND validation all scopes in the `allowed_scopes` param need to be present in the jwt scope and in the OR if any scope is present that\'s enough. You can receive the token content if you want by setting `token_content` to `True` this will inject the param `token_content: dict` into your function as `kwargs`\n\n```python\nimport auth2guard\n\n\nclass Request:\n    def __init__(self, headers: dict):\n        self._headers = headers\n\n    @property\n    def headers(self) -> dict:\n        return self._headers\n\n\nauth2guard.set_config(jwk=\'{"p":"-7pCvLlzsNIRD7utbLZqB...\')\n\n\n@auth2guard.validate(\n    allowed_scopes=["test1"], \n    scope_and_validation=True, \n    inject_token_content=True,\n    allowed_audiences=["test1"],\n    audience_and_validation=True\n)\ndef route_callback(request, token_content: dict):\n    pass\n\n\nrequest = Request(headers={"Authorization": f"Basic XXX"})\nroute_callback(request=request)\n```',
    'author': 'Marco Sievers de Almeida Ximit Gaia',
    'author_email': 'im.ximit@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
