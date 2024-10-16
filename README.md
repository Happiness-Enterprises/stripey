# Common Utility Methods

This is a collection of utility methods and classes that are helpful across an array of Python projects.

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

Once the `pip.conf` and `.netrc` files are ready, simply run installations as you normally would. For example:

```sh
pip install happy-common-utils
```
