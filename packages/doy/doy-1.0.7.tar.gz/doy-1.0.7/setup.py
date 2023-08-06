# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doy', 'doy..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2', 'numpy', 'rich>=13.4.1', 'tqdm>=4.65.0']

setup_kwargs = {
    'name': 'doy',
    'version': '1.0.7',
    'description': '',
    'long_description': '# Doy\n\nSimple utility package\n',
    'author': 'Dominik Schmidt',
    'author_email': 'schmidtdominik30@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
