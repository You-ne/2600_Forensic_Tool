# About Poetry usage

Besides the installation of `poetry` and `fouine`, there is __3 commands__ that will be useful for interacting with `poetry`:

- `poetry shell` will launch a shell with the poetry virtual environment activated.
- `exit` to quit the poetry shell.
- `poetry run cmd` to run a command inside poetry shell without entering poetry shell.

For anything else check [the official poetry documentation](https://python-poetry.org/docs) ;)

# For Users

## Installation

First install `Poetry` with the following command:
    `. ./installer_poetry/poetry_install.sh`

To remove it, simply use the script:
    `./installer_poetry/poetry_uninstall.sh`

You can now install the project and the required dependencies with `poetry install`.


# For Devs

## Installation

First install `Poetry` with the following command:

`. ./installer_poetry/poetry_install.sh`

To remove it, simply use the script:

`./installer_poetry/poetry_uninstall.sh`

<br>

You can now install the project and the required dependencies with `poetry install`.

To install optional dependencies with it, use the option `--with group`. Actually, there is 2 optionnal dependencies groups: `docs` and `dev`.

Install `fouine` with the following to have everything needed for contribution at hand:

   `poetry install --with dev,doc`

<br>

You can add a dependend to the project with:

`poetry add pkg`

Or to a specific dependencies group with:

`poetry add pkg -G group`

## Committing

When committing for the 1st time after cloning, install pre-commit hookw with `pre-commit install`

They will run automatically before each commit, on staged files.
If these tools checks are failing, you won't be able to commit...

So correct your style !

You can skip the checks with the option `--no-verify` when committing.

Or run the hooks without committing with `pre-commit run --all`.