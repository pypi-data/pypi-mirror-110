# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funktion']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'funktion',
    'version': '0.1.0',
    'description': 'Create and deploy functions to your own servers easily.',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
