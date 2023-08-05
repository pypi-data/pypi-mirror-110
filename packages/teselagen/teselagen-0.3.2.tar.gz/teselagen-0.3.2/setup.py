# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teselagen',
 'teselagen.api',
 'teselagen.api.tests',
 'teselagen.examples',
 'teselagen.utils']

package_data = \
{'': ['*'],
 'teselagen': ['.mypy_cache/*',
               '.mypy_cache/3.6/*',
               '.mypy_cache/3.6/_typeshed/*',
               '.mypy_cache/3.6/collections/*',
               '.mypy_cache/3.6/email/*',
               '.mypy_cache/3.6/http/*',
               '.mypy_cache/3.6/importlib/*',
               '.mypy_cache/3.6/json/*',
               '.mypy_cache/3.6/logging/*',
               '.mypy_cache/3.6/os/*',
               '.mypy_cache/3.6/requests/*',
               '.mypy_cache/3.6/requests/packages/*',
               '.mypy_cache/3.6/requests/packages/urllib3/*',
               '.mypy_cache/3.6/requests/packages/urllib3/packages/*',
               '.mypy_cache/3.6/requests/packages/urllib3/packages/ssl_match_hostname/*',
               '.mypy_cache/3.6/requests/packages/urllib3/util/*',
               '.mypy_cache/3.6/teselagen/*',
               '.mypy_cache/3.6/teselagen/api/*',
               '.mypy_cache/3.6/teselagen/utils/*',
               '.mypy_cache/3.6/urllib/*'],
 'teselagen.examples': ['.ipynb_checkpoints/*',
                        '_dev/*',
                        '_dev/.ipynb_checkpoints/*',
                        'pytested/*',
                        'pytested/.ipynb_checkpoints/*']}

install_requires = \
['dna_features_viewer>=3.0.3,<4.0.0',
 'fastaparser>=1.1,<2.0',
 'pandas>=1.0.0,<2.0.0',
 'pytest-cov>=2.8.1,<3.0.0',
 'pytest-notebook>=0.6.1,<0.7.0',
 'pytest-xdist>=1.31.0,<2.0.0',
 'pytest>=5.3.5,<6.0.0',
 'requests-mock>=1.8,<2.0',
 'requests>=2.22.0,<3.0.0',
 'setuptools>=45.1.0,<46.0.0',
 'single_version>=1.5.1,<2.0.0',
 'tqdm>=4.53.0,<5.0.0']

setup_kwargs = {
    'name': 'teselagen',
    'version': '0.3.2',
    'description': 'Teselagen Biotechnology API client',
    'long_description': '# TeselaGen Python Tools.\n\nThis package includes some Python tools to use in combination with TeselaGen platform.\nThese tools includes _TeselaGen Python API Client_ \n\nThis package runs on Python 3.6 and above.\n\n**NOTE :** All the following commands are supposed to be run on the `base` directory, unless specified.\n\n## Library Installation\nThis library contains the TeselaGen Python API Client.\n\nTo install it locally,\n\n1. By using PIP\n\n    Use `pip install teselagen`\n\n\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TeselaGen/api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
