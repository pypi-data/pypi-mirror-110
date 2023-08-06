# slurm_in_aws

[![](docs/img/badges/language.svg)](https://devdocs.io/python/)

Mock EC2 with moto + launch instances in Docker.

## Usage

```sh
# TODO
```

## Contributing

### Contributing Setup

1. Clone the project locally
1. Install the corresponding [.python-version](./.python-version) using something like [pyenv](https://github.com/pyenv/pyenv)
1. Create a virtual environment named `.venv` with `python -m venv .venv`
1. Activate the virtual environment with `source .venv/bin/activate`
1. Install [poetry](https://poetry.eustace.io/docs/#installation)
1. Install [invoke](https://www.pyinvoke.org/installing.html) with `pip install invoke`
1. Run `poetry install --no-root`
1. Run `invoke setup`

### Contributing Tests

Run `poetry run invoke tests`

### Contributing All Checks (including tests)

Run `poetry run invoke hooks`

### Build And Publish to PyPI

```sh
poetry build
poetry publish
```
