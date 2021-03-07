# Jupyter Packaging

Tools to help build and install Jupyter Python packages that require a pre-build step that may include JavaScript build steps.

## Install

`pip install jupyter-packaging`

## Usage

There are three ways to use `jupyter-packaging` in another package.

1. Use a `pyproject.toml` file as outlined in [pep-518](https://www.python.org/dev/peps/pep-0518/).
An example:

```toml
[build-system]
requires = ["jupyter_packaging~=0.8.0"]
build-backend = "setuptools.build_meta"
```

Below is an example `setup.py` that uses the `pyproject.toml` approach.  It assumes the rest of your metadata is in [`setup.cfg`](https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html):

```py
from setuptools import setup

try:
    from jupyter_packaging import wrap_installers, npm_builder
    cmdclass = wrap_installers(npm_builder())
except ImportError:
    cmdclass = {}

setup(cmdclass=cmdclass))
```

2. Use the `jupyter_packaging` build backend.
The pre-build command is specified as metadata in `pyproject.toml`:

```toml
[build-system]
requires = ["jupyter_packaging~=0.8.0"]
build-backend = "jupyter_packaging.build_api"

[tool.jupyter-packaging.builder]
func = "jupyter_packaging.npm_builder"

[tool.jupyter-packaging.build-args]
build_cmd = "build:src"
```

The corresponding `setup.py` would be greatly simplified:

```py
from setuptools import setup
setup()
```

The build backend does not handle the `develop` command (`pip install -e .`).
If desired, you can wrap just that command (note the use of `wrap_dist=False`):

```py
import setuptools

try:
    from jupyter_packaging import wrap_installers, npm_builder
    builder = npm_builder(build_cmd="build:dev")
    cmdclass = wrap_installers(builder, wrap_dist=False)
except ImportError:
    cmdclass = {}

setup(cmdclass=cmdclass))
```

3. Vendor `setupbase.py` locally alongside `setup.py` and import the module directly.

```py
import setuptools
from setupbase import wrap_installers, npm_builder
cmdclass = wrap_installers(npm_builder())
setup(cmdclass=cmdclass)
```

## Usage Notes

- We recommend using `include_package_data=True` and `MANIFEST.in` to control the assets used in the [dist files](https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html).
- Tools like [`check-manifest`](https://github.com/mgedmin/check-manifest) or [`manifix`](https://github.com/vidartf/manifix) can be used to ensure the desired assets are shipped.
- Python `data_files` are not supported in `develop` mode.  You can work around this limitation by doing a full install (`pip install .`) before the develop install (`pip install -e .`), or by adding a script to push the data files to `sys.base_prefix`.


## Development Install

```bash
git clone https://github.com/jupyter/jupyter-packaging.git
cd jupyter-packaging
pip install -e .
```

You can test changes locally by creating a `pyproject.toml` with the following, replacing the local path to the git checkout:

```toml
[build-system]
requires = ["jupyter_packaging@file://<path-to-git-checkout>"]
build-backend = "setuptools.build_meta"
```

Note that you need to run `pip cache remove jupyter_packaging` any time changes are made to prevent `pip` from using a previous source version.
