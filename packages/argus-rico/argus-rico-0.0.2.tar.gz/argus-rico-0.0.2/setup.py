# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['argus_rico', 'argus_rico.models']

package_data = \
{'': ['*'], 'argus_rico': ['schemas/*']}

install_requires = \
['astropy>=5.3,<6.0',
 'black>=23.3.0,<24.0.0',
 'blosc>=1.11.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'confluent-kafka>=2.1.1,<3.0.0',
 'fastapi>=0.95.2,<0.96.0',
 'fastavro>=1.4.12,<2.0.0',
 'geojson-pydantic>=0.6.2,<0.7.0',
 'ipython>=8.14.0,<9.0.0',
 'numpy>=1.24.3,<2.0.0',
 'orjson>=3.8.13,<4.0.0',
 'pyarrow>=10.0.0',
 'pydantic>=1.10.8,<2.0.0',
 'pymongo>=4.3.3,<5.0.0',
 'pymongoarrow>=0.7.0,<0.8.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'rich>=13.3.5,<14.0.0',
 'sanitize-filename>=1.2.0,<2.0.0',
 'slack-bolt>=1.18.0,<2.0.0']

entry_points = \
{'console_scripts': ['rico = rico.cli:main']}

setup_kwargs = {
    'name': 'argus-rico',
    'version': '0.0.2',
    'description': 'Transient alert generation and database interaction for Argus and Evryscope',
    'long_description': None,
    'author': 'Hank Corbett',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
