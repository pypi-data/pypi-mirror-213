# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbnomics_data_model',
 'dbnomics_data_model.model',
 'dbnomics_data_model.scripts',
 'dbnomics_data_model.storage',
 'dbnomics_data_model.storage.adapters',
 'dbnomics_data_model.storage.adapters.filesystem',
 'dbnomics_data_model.storage.adapters.filesystem.model',
 'dbnomics_data_model.storage.adapters.filesystem.model.json_lines_variant',
 'dbnomics_data_model.storage.adapters.filesystem.model.tsv_variant']

package_data = \
{'': ['*']}

install_requires = \
['daiquiri>=3.0.1,<4.0.0',
 'dirsync>=2.2.5,<3.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'orjson>=3.6.7,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pysimdjson>=4.0.3,<5.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'toolz>=0.11.2,<0.12.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['dbnomics-update-storage = '
                     'dbnomics_data_model.scripts.update_storage:app',
                     'dbnomics-validate-storage = '
                     'dbnomics_data_model.scripts.validate_storage:app']}

setup_kwargs = {
    'name': 'dbnomics-data-model',
    'version': '0.13.34',
    'description': 'Provide classes for DBnomics entities and a storage abstraction',
    'long_description': '# DBnomics Data Model\n\nIn DBnomics, once data has been downloaded from providers, it is converted in a common format: the DBnomics data model.\n\nThis Python package provides:\n\n- model classes defining DBnomics entities (provider, dataset, series, etc.) with their business logic and validation rules\n- a data storage abstraction to load and save those entities\n- adapters implementing the data storage abstraction (e.g. `dbnomics_data_model.storage.adapters.filesystem`)\n\nThis package is used in particular by the convert script of fetchers in order to save data.\n\n## Documentation\n\nPlease read <https://db.nomics.world/docs/data-model/>\n\n## Validate data\n\nTo validate a directory containing data written by (or compatible with) the "filesystem" adapter:\n\n```sh\ndbnomics-validate-storage <storage_dir>\n```\n\nThis script outputs the data validation errors it finds.\n\n## Run tests\n\nTo run unit tests:\n\n```sh\npytest\n```\n\nCode quality:\n\n```sh\nflake8 .\n```\n\nSee also: <https://git.nomics.world/dbnomics-fetchers/documentation/wikis/code-style>\n\n## Publish a new version\n\nFor package maintainers:\n\n```bash\ngit tag x.y.z\ngit push\ngit push --tags\n```\n\nGitLab CI will publish the package to <https://pypi.org/project/dbnomics-data-model/> (see [`.gitlab-ci.yml`](./.gitlab-ci.yml)).\n',
    'author': 'DBnomics Team',
    'author_email': 'contact@nomics.world',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.nomics.world/dbnomics/dbnomics-data-model',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
