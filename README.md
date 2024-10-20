# Common Utility Methods

This is a collection of utility methods and classes that are helpful across an array of Python projects.

# Setup

Setting up for development is simple using the `setup.sh` script. It will create a virtual environment and tell you how to activate it.

# Build

To perform a build, just run the `build.sh` script. To change any build settings, modify `pyproject.toml`.

By default, `build.sh` builds code in `dev` mode, which means any version tags have `dev` in the name. You may also pass `-r` or `--release` to `build.sh`, and it will create a build without the `dev` tag, indicating it is ready for release.

# Publish

Create `${HOME}/.pypirc` with the following contents:

```ini
[pypi]
repository = https://pypi.happystl.com/
username = <username>
password = <password>
```

Make sure you set the file permissions correctly e.g. `chmod 0600 "${HOME}/.pypirc"`. Then you can use the `publish.sh` script to push any of your builds to the pypi repo.

# Install

Install the package as either a live-edit installation or a normal installation. If you would like to try one mode and then another, please uninstall first.

## Live-Edit Installation

If you are a developer, you will want to install this package in live-edit mode. This is like installing the package in the normal way, except any changes performed in the package are reflected immediately by any code that does `import my_pkg`. Simply run:

```sh
pip install -e .
```

## Normal Installation

Create `${HOME}/.config/pip/pip.conf` with the following contents:

```ini
[global]
index-url = https://pypi.happystl.com/simple/
```

Create `${HOME}/.netrc` with the following contents:

    machine pypi.happystl.com
    login <username>
    password <password>

Make sure you set the file permissions correctly e.g. `chmod 0600 "${HOME}/.netrc"`.

Once the `pip.conf` and `.netrc` files are ready, install the package normally:

```sh
pip install happy-common-utils
```
