# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylsp_mypy_rnx']

package_data = \
{'': ['*']}

install_requires = \
['pkg_resources', 'python-lsp-server>=1.0,<2.0']

entry_points = \
{'pylsp': ['pylsp_mypy_rnx = pylsp_mypy_rnx.plugin']}

setup_kwargs = {
    'name': 'pylsp-mypy-rnx',
    'version': '0.1.0',
    'description': 'mypy-ls fork for more options',
    'long_description': '# pylsp-mypy-rnx\n\n[![Build Status](https://travis-ci.com/gjeusel/pylsp-mypy-rnx.svg?branch=master)](https://travis-ci.com/gjeusel/pylsp-mypy-rnx)\n[![Codecov](https://codecov.io/gh/gjeusel/pylsp-mypy-rnx/branch/master/graph/badge.svg)](https://codecov.io/gh/gjeusel/pylsp-mypy-rnx)\n[![PyPI](https://badge.fury.io/py/pylsp-mypy-rnx.svg)](https://pypi.python.org/pypi/pylsp-mypy-rnx/)\n\nmypy-ls fork\n\n\n## Installation\n\n``` bash\npip install pylsp-mypy-rnx\n```\n\n\n## Develop\n```bash\npoetry install\npoetry run pre-commit install -t pre-push\n```\n',
    'author': 'Guillaume Jeusel',
    'author_email': 'guillaume.jeusel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gjeusel/pylsp-mypy-rnx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
