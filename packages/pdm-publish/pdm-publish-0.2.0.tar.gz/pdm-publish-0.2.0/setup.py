# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdm_publish']

package_data = \
{'': ['*']}

install_requires = \
['pdm>=1,<2', 'twine>=3,<4']

entry_points = \
{'pdm': ['publish = pdm_publish.__init__:main']}

setup_kwargs = {
    'name': 'pdm-publish',
    'version': '0.2.0',
    'description': 'A PDM plugin to publish to PyPI',
    'long_description': None,
    'author': 'Branch Vincent',
    'author_email': 'branchevincent@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/branchvincent/pdm-publish',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
