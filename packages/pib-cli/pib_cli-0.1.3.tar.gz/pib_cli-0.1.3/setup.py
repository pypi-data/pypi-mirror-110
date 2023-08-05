# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pib_cli', 'pib_cli.config', 'pib_cli.patchbay', 'pib_cli.support']

package_data = \
{'': ['*'], 'pib_cli': ['bash/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'bandit>=1.7.0,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'commitizen>=2.7.16,<3.0.0',
 'isort>=5.8.0,<6.0.0',
 'jinja2>=2.11.3,<3.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pydocstyle>=6.1.1,<7.0.0',
 'pylint>=2.8.3,<3.0.0',
 'pytest-cov>=2.12.1,<3.0.0',
 'pytest-pylint>=0.18.0,<0.19.0',
 'pytest>=6.2.4,<7.0.0',
 'safety>=1.10.3,<2.0.0',
 'wheel>=0.36.2,<0.37.0',
 'yamllint>=1.25.0,<2.0.0',
 'yapf>=0.31.0,<0.32.0']

extras_require = \
{'docs': ['sphinx>=4.0.2,<5.0.0', 'sphinx-autopackagesummary>=1.3,<2.0'],
 'pib_docs': ['sphinx>=4.0.2,<5.0.0',
              'sphinx-autopackagesummary>=1.3,<2.0',
              'sphinx-click>=3.0.0,<4.0.0',
              'sphinx-jsonschema>=1.16.8,<2.0.0'],
 'types': ['mypy>=0.902,<0.903']}

entry_points = \
{'console_scripts': ['dev = pib_cli.cli:cli', 'pib_cli = pib_cli.cli:cli']}

setup_kwargs = {
    'name': 'pib-cli',
    'version': '0.1.3',
    'description': 'Python Development CLI',
    'long_description': '# PIB CLI\n\nA development environment CLI, complete with tooling.\n\n[Project Documentation](https://pib_cli.readthedocs.io/en/latest/)\n\n## Master Branch\n\n[![pib_cli-automation](https://github.com/shared-vision-solutions/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=master)](https://github.com/shared-vision-solutions/pib_cli/actions)\n\n## Production Branch\n\n[![pib_cli-automation](https://github.com/shared-vision-solutions/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=production)](https://github.com/shared-vision-solutions/pib_cli/actions)\n\n## Supported Python Versions\n\nTested to work under the following python version:\n- Python 3.7\n- Python 3.8\n- Python 3.9\n\n## Installation\n\nThis is a development environment CLI, with a customizable yaml config.\n\nIt\'s built into this [Cookie Cutter](https://github.com/cookiecutter/cookiecutter) template:\n\n- [Python In A Box](https://github.com/shared-vision-solutions/python-in-a-box)\n\nTo install, simply use: \n- `pip install pib_cli`\n- `pip install pib_cli[docs]` (Adds [Sphinx](https://www.sphinx-doc.org/en/master/) support.)\n- `pip install pib_cli[types]` (Adds [MyPy](http://mypy-lang.org/) support.)\n\n## Usage\n\n- use the `dev` command for details once installed\n\n## Container\n\n[python:3.7-slim](https://github.com/docker-library/python/tree/master/3.7/buster/slim)\n\n## License\n\n[MPL-2](LICENSE)\n\n## Included Packages\n\nAfter using `pib_cli` on a number of projects I realized there is not a one size fits all solution.  \n\n- Some projects require extensive documentation, some projects require typing, some do not.\n- At the suggestion of a friend, I\'ve grouped the installable packages into "extras", that you can choose to install alongside the core `pib_cli` install.\n\n### Core Installed Packages:\n| package    | Description                       |\n| ---------- | --------------------------------- |\n| bandit     | Finds common security issues      |\n| commitizen | Standardizes commit messages      |\n| isort      | Sorts imports                     |\n| poetry     | Python Package Manager            |\n| pydocstyle | PEP 257 enforcement               |\n| pylint     | Static Code Analysis              |\n| pytest     | Test suite                        |\n| pytest-cov | Coverage support for pytest       |\n| safety     | Dependency vulnerability scanning |\n| wheel      | Package distribution tools        |\n| yamllint   | Lint yaml configuration files     |\n| yapf       | Customizable Code Formatting      |\n\n- `poetry install` to install only these dependencies.\n- This is the base install, and you\'ll always get these dependencies installed.\n\n### \'types\' extras:\n| package    | Description                       |\n| ---------- | --------------------------------- |\n| mypy       | Static type checker               |\n\n- `poetry install -E types` to add these dependencies to the core installation.\n\n### \'docs\' extras:\n| package    | Description                       |\n| ---------- | --------------------------------- |\n| sphinx     | Generating documentation          |\n| sphinx-autopackagesummary | Template nested module content |\n\n- `poetry install -E docs` to add these dependencies to the core installation.\n\n### \'pib_docs\' extras:\n| package    | Description                       |\n| ---------- | --------------------------------- |\n| sphinx     | Generating documentation          |\n| sphinx-autopackagesummary | Template nested module content     |\n| sphinx-click              | Generate cli documentation         |\n| sphinx-jsonschema         | Generate schema documentation      |\n\n- `poetry install -E pib_docs` to add these dependencies to the core installation.\n- These extras exist only to support building `pib_cli`\'s documentation- they aren\'t meant to be consumed by user projects.\n\n### Installing Multiple Extras:\n\nThis is straight-forward to do:\n- `poetry install -E docs -E types`\n\n## Customizing the Command Line Interface\n\nThe CLI has some defaults built in, but is customizable by setting the `PIB_CONFIG_FILE_LOCATION` environment variable.\nThe default config file can be found [here](pib_cli/config/config.yml).\n\nEach command is described by a yaml key in this format :\n\n```yaml\n- name: "command-name"\n  path_method: "location_string"\n  commands:\n    - "one or more"\n    - "shell commands"\n    - "each run in a discrete environment"\n  success: "Success Message"\n  failure: "Failure Message"\n```\n\nwhere `location_string` is one of:\n\n- `project_root` (`/app`)\n- `project_docs` (`/app/documentation`)\n- `project_home` (`/app/${PROJECT_HOME}`)\n\n## Installing a virtual environment, and the CLI on your host machine\n\nThe [scripts/extras.sh](scripts/extras.sh) script does this for you.\n\nFirst install [poetry](https://python-poetry.org/) on your host machine:\n- `pip install poetry`\n\nThen source this script, setup the extras, and you can use the `dev` command on your host:\n- `source scripts/extras.sh`\n- `pib_setup_hostmachine` (to install the poetry dependencies)  \n- `dev --help` (to run the cli outside the container)\n\nThis is most useful for making an IDE like pycharm aware of what\'s installed in your project.\n\n> It is still recommended to work inside the container, as you\'ll have access to the full managed python environment, \n> as well as any additional services you are running in containers.  \n\nIf you wish to use the cli outside the container for all tasks, [tomll](https://github.com/pelletier/go-toml) and [gitleaks](https://github.com/zricethezav/gitleaks) will also need to be installed, or the [cli.yml](./assets/cli.yml) configuration will need to be customized to remove these commands.\n\n## Development Guide for `pib_cli`\n\nPlease see the documentation [here](./CONTRIBUTING.md).\n',
    'author': 'Niall Byrne',
    'author_email': 'niall@niallbyrne.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shared-vision-solutions/pib_cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
