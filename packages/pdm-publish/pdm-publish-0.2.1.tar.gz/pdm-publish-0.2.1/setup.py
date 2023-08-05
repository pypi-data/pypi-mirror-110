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
    'version': '0.2.1',
    'description': 'A PDM plugin to publish to PyPI',
    'long_description': "# PDM Publish\n\n[![ci](https://github.com/branchvincent/pdm-publish/workflows/CI/badge.svg)](https://github.com/branchvincent/pdm-publish/actions/workflows/ci.yaml)\n[![pypi version](https://img.shields.io/pypi/v/pdm-publish.svg)](https://pypi.org/project/pdm-publish/)\n[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\nA PDM plugin to publish to PyPI\n\n> NOTE: Consider if you need this over using [twine](https://twine.readthedocs.io/) directly\n\n## Installation\n\nIf you installed `pdm` via `pipx`:\n\n```sh\npipx inject pdm pdm-publish\n```\n\nor `brew`:\n\n```sh\n$(brew --prefix pdm)/libexec/bin/python -m pip install pdm-publish\n```\n\nor `pip`:\n\n```sh\npip install --user pdm-publish\n```\n\n## Usage\n\n`pdm-publish` enables `pdm` to publish packages to PyPI by wrapping [twine](https://twine.readthedocs.io/en/latest/) internally.\nFor example, to build and publish:\n\n```sh\n# Using token auth\npdm publish --password token\n# To test PyPI using basic auth\npdm publish -r testpypi -u username -P password\n# To custom index\npdm publish -r https://custom.index.com/\n```\n\nFull usage:\n\n```sh\n$ pdm publish --help\nUpload artifacts to a remote repository\n\nUsage:\n\nOptions:\n  -h, --help            show this help message and exit\n  -v, --verbose         -v for detailed output and -vv for more detailed\n  -g, --global          Use the global project, supply the project root with\n                        `-p` option\n  -p PROJECT_PATH, --project PROJECT_PATH\n                        Specify another path as the project root, which\n                        changes the base of pyproject.toml and __pypackages__\n  -r REPOSITORY, --repository REPOSITORY\n                        The repository name or url to publish the package to\n                        [env var: PDM_PUBLISH_REPO]\n  -u USERNAME, --username USERNAME\n                        The username to access the repository [env var:\n                        PDM_PUBLISH_USERNAME]\n  -P PASSWORD, --password PASSWORD\n                        The password to access the repository [env var:\n                        PDM_PUBLISH_PASSWORD]\n  --dry-run             Perform all actions except upload the package\n  --no-build            Don't build the package before publishing\n```\n\n## Configuration\n\n| Config Item        | Description                           | Default Value | Available in Project | Env var                |\n| ------------------ | ------------------------------------- | ------------- | -------------------- | ---------------------- |\n| `publish.repo`     | PyPI repo name (pypi/testpypi) or url | `pypi`        | True                 | `PDM_PUBLISH_REPO`     |\n| `publish.username` | PyPI username                         | `__token__`   | True                 | `PDM_PUBLISH_USERNAME` |\n| `publish.password` | PyPI password                         |               | True                 | `PDM_PUBLISH_PASSWORD` |\n\n## Links\n\n- [Changelog](https://github.com/branchvincent/pdm-publish/releases)\n- [Contributing](CONTRIBUTING.md)\n",
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
