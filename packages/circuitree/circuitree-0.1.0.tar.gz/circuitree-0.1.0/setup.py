# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circuitree']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.1,<4.0', 'numpy>=1.23.0,<2.0.0']

setup_kwargs = {
    'name': 'circuitree',
    'version': '0.1.0',
    'description': 'Genetic circuit design using Monte Carlo tree search',
    'long_description': '# CircuiTree\nGenetic circuit design using Monte Carlo tree search\n\n## Installation\n\n### From a package repository\n[Installation with `pip`/`conda` is not yet supported]\n\n### From the GitHub repository\n\nTo install and use `circuitree` from the GitHub source code, first clone the repo into a directory.\n\n```git clone https://github.com/pranav-bhamidipati/circuitree.git[ dir_name]```\n\nThen, enter the directory and build the environment using the command-line tool `poetry`. Instructions for installation can be [found here](https://python-poetry.org/). by running `poetry install`. This will install a virtual environment in the virtualenv cache directory `POETRY_CACHE_DIR`. To activate this environment interactively as a nested shell, run `poetry shell`. Alternatively, you can run a command in the virtual environment with `poetry run <command>`. \n\nFor instance, to launch a Jupyter notebook with `circuitree` pre-loaded, run `poetry run jupyter notebook`.\n\n## Usage\n\nSee the [quick-start demo](examples/quick_start.ipynb).\n',
    'author': 'pranav-bhamidipati',
    'author_email': 'pbhamidi@usc.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
