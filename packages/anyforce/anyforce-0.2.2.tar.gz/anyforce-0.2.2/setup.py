# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anyforce',
 'anyforce.api',
 'anyforce.dynamic',
 'anyforce.json',
 'anyforce.model',
 'anyforce.request']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['fastapi>=0.65.2,<0.66.0',
 'orjson>=3.5.3,<4.0.0',
 'passlib[bcrypt]>=1.7.4,<2.0.0',
 'pydantic[email]>=1.8.2,<2.0.0',
 'python-jose[cryptography]>=3.2.0,<4.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.25.1,<3.0.0',
 'tortoise-orm[aiomysql]>=0.17.4,<0.18.0',
 'uvicorn[standard]>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'anyforce',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'exherb',
    'author_email': 'i@4leaf.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
