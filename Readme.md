# Fouine

This is '__fouine__', a _forensic tool_.


---


## About Poetry usage

Besides the installation of _poetry_ and _fouine_, there is 3 commands that will be useful for interacting with _poetry_:

- `poetry shell` will launch a shell with the poetry virtual environment activated. `poetry install` may launch it.

- `exit` to quit the __poetry shell__.

- `poetry run cmd` to run a command inside poetry shell without entering it.


For anything else check __https://python-poetry.org/docs__ ;)


---


## For Users


### Installation

First install Poetry with the following command:


        . ./installer_poetry/poetry_install.sh



To remove it, simply use the script:


        ./installer_poetry/poetry_uninstall.sh



You can now install the project and the required dependencies with `poetry install`.


---


## For Devs


### Installation

First install Poetry with the following command:


        . ./installer_poetry/poetry_install.sh



To remove it, simply use the script:


        ./installer_poetry/poetry_uninstall.sh



You can now install the project and the required dependencies with `poetry install`.

To install optional dependencies with it, use the option `--with group`.
Actually, there is 2 optionnal dependencies groups: `doc` and `dev`.

Install __fouine__ with the following to have everything needed for contribution at hand:


        poetry install --with dev,doc


### Committing

When committing to the repo, the hooks configured by __pre-commit__ will be used on the codebase to check it's conformity.

If these tools checks are failing, you won't be able to commit...

So correct your style !

---

## Documentation

After cloning the repo, and installing with:
`poetry install --with docs`

Run `mkdocs build` and `mkdocs serve`.

You will have access to the documentation on [localhost](http://localhost:8000)
It is much more extensive than this poor README ;)

