# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypothesis_faker', 'hypothesis_faker.providers']

package_data = \
{'': ['*']}

install_requires = \
['faker>=8.8.1,<9.0.0', 'hypothesis>=6.14.0,<7.0.0']

setup_kwargs = {
    'name': 'hypothesis-faker',
    'version': '0.0.23',
    'description': 'Some faker providers ported as hypothesis strategies',
    'long_description': None,
    'author': 'Derek Wan',
    'author_email': 'd.wan@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dycw/hypothesis-faker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
