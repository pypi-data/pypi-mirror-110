# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pickax']

package_data = \
{'': ['*']}

install_requires = \
['jax>=0.2.14,<0.3.0', 'jaxlib>=0.1.67,<0.2.0']

setup_kwargs = {
    'name': 'pickax',
    'version': '2021.6.0',
    'description': 'A library for creating neural networks in python based on jax',
    'long_description': None,
    'author': 'Matt LeMay',
    'author_email': 'mplemay@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
