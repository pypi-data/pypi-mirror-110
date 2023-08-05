# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vjemmieapi',
 'vjemmieapi.crud',
 'vjemmieapi.exceptions',
 'vjemmieapi.models',
 'vjemmieapi.public',
 'vjemmieapi.schemas']

package_data = \
{'': ['*']}

install_requires = \
['aiomysql>=0.0.21,<0.0.22',
 'fastapi>=0.65.1,<0.66.0',
 'sqlalchemy>=1.4.18,<2.0.0',
 'uvicorn[standard]>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'vjemmieapi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Peder Hovdan Andresen',
    'author_email': 'pedeha@stud.ntnu.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
