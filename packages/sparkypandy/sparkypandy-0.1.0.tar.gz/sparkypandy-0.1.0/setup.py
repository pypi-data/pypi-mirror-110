# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sparkypandy']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.4,<2.0.0', 'pyspark>=3.1.2,<4.0.0']

setup_kwargs = {
    'name': 'sparkypandy',
    'version': '0.1.0',
    'description': "It's not spark, it's not pandas, it's just awkward...",
    'long_description': None,
    'author': 'Tomas Pereira de Vasconcelos',
    'author_email': 'tomasvasconcelos1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
