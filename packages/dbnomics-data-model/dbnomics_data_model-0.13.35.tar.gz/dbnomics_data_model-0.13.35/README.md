# DBnomics Data Model

In DBnomics, once data has been downloaded from providers, it is converted in a common format: the DBnomics data model.

This Python package provides:

- model classes defining DBnomics entities (provider, dataset, series, etc.) with their business logic and validation rules
- a data storage abstraction to load and save those entities
- adapters implementing the data storage abstraction (e.g. `dbnomics_data_model.storage.adapters.filesystem`)

This package is used in particular by the convert script of fetchers in order to save data.

## Documentation

Please read <https://db.nomics.world/docs/data-model/>

## Validate data

To validate a directory containing data written by (or compatible with) the "filesystem" adapter:

```sh
dbnomics-validate-storage <storage_dir>
```

This script outputs the data validation errors it finds.

## Run tests

To run unit tests:

```sh
pytest
```

Code quality:

```sh
flake8 .
```

See also: <https://git.nomics.world/dbnomics-fetchers/documentation/wikis/code-style>

## Publish a new version

For package maintainers:

```bash
git tag x.y.z
git push
git push --tags
```

GitLab CI will publish the package to <https://pypi.org/project/dbnomics-data-model/> (see [`.gitlab-ci.yml`](./.gitlab-ci.yml)).
