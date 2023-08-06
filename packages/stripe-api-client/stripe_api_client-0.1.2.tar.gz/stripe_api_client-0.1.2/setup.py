# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stripe_api_client', 'stripe_api_client.resources']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'stripe-api-client',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'Steven Athouel',
    'author_email': 'sathouel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
