# Ingot Ingot Sql package.

Provides SQS functionality for Ingots projects.

## For consumers

For using the Ingot package just execute the following commands:
* Add the package to the `requirements.txt` file of your project.
* Install int using the `pip` tool.
* TODO. Add here something extra information.

### Package CLI

The package provides CLI.
It allows to start working with the package quickly.
It contains the following commands:
TODO. Add builders here after generating their by the `ingots package_bootstrap` tool.

For using the CLI tool just call the following command:
```bash
ingot-sql-cli <command>
```
Getting package CLI help:
```bash
ingot-sql-cli --help
ingot-sql-cli <command> --help
```

## For developers

### Prepare the project for working

Clone a repository:
```bash
mkdir ingots-libs
cd ingots-libs
git clone https://github.com/ABKorotky/ingot-sql.git
cd ingot-sql
```

Prepare a virtual environment:
```bash
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Prepare repository hooks
```bash
pip install pre_commit
pre-commit install
pre-commit autoupdate
```

Configure code-quality tools:
```bash
pip install black flake8 mypy coverage
```

Configure the Sphinx tool

Please, use the following page for configuring the Sphinx documentation generator: [Sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html)
```bash
pip install sphinx
sphinx-build -b html docs docs/build -v
```

### Using the tox tool

The Ingot package allows automation via the `tox` tool.
```bash
pip install tox
```

Use configured tox tool for several activities.

`tox -e reformat` - auto reformat code by the black tool, makes ordering import too.

`tox -e cs` - checks code style by PEP8.

`tox -e ann` - checks annotations of types by the mypy tool.

`tox -e utc` - runs unittests with the coverage tool.

`tox -e report` - builds coverage report for the project.

`tox -e doc` - builds a package documentation.

`tox -e build` - builds a package form current branch / tag / commit.

`tox -e upload` - uploads package to the PyPI index. Set the `PYPI_REPOSITORY_ALIAS` virtual variable for specify PyPI destination.

Calling tox without parameters will execute the following steps: **cs**, **ann**, **utc** and **report**.

### Using package CLI locally
Obviously, it's impossible to call the package CLI via package entry-point.

Use the following command instead:
```bash
python -m ingot_sql.scripts.ingot_sql ...
```
