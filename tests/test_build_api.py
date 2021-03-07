import os
import sys
from unittest.mock import patch, call

import pytest

from jupyter_packaging.build_api import build_wheel, build_sdist


TOML_CONTENT = """
[tool.jupyter-packaging.builder]
func = "foo.main"

[tool.jupyter-packaging.build-args]
fizz = "buzz"
"""


BAD_CONTENT = """
[tool.jupyter-packaging.builder]
bar = "foo.main"
"""


FOO_CONTENT = r"""
from pathlib import Path
def main(fizz=None):
    Path('foo.txt').write_text(f'fizz={fizz}', encoding='utf-8')
"""


def test_build_wheel_no_toml(tmp_path):
    os.chdir(tmp_path)
    with patch('jupyter_packaging.build_api.orig_build_wheel') as orig_wheel:
        build_wheel(tmp_path)
        orig_wheel.assert_called_with(tmp_path, config_settings=None, metadata_directory=None)


def test_build_wheel(tmp_path):
    os.chdir(tmp_path)
    tmp_path.joinpath('foo.py').write_text(FOO_CONTENT)
    sys.path.insert(0, str(tmp_path))
    tmp_path.joinpath('pyproject.toml').write_text(TOML_CONTENT, encoding='utf-8')
    with patch('jupyter_packaging.build_api.orig_build_wheel') as orig_wheel:
        build_wheel(tmp_path)
        orig_wheel.assert_called_with(tmp_path, config_settings=None, metadata_directory=None)
        data = tmp_path.joinpath('foo.txt').read_text(encoding='utf-8')
        assert data == 'fizz=buzz'


def test_build_wheel_bad_metadata(tmp_path):
    os.chdir(tmp_path)
    os.chdir(tmp_path)
    tmp_path.joinpath('foo.py').write_text(FOO_CONTENT)
    sys.path.insert(0, str(tmp_path))
    tmp_path.joinpath('pyproject.toml').write_text(BAD_CONTENT, encoding='utf-8')
    with patch('jupyter_packaging.build_api.orig_build_wheel') as orig_wheel:
        with pytest.raises(ValueError):
            build_wheel(tmp_path)
        orig_wheel.assert_not_called()


def test_build_wheel_no_toml(tmp_path):
    os.chdir(tmp_path)
    with patch('jupyter_packaging.build_api.orig_build_wheel') as orig_wheel:
        build_wheel(tmp_path)
        orig_wheel.assert_called_with(tmp_path, config_settings=None, metadata_directory=None)


def test_build_sdist(tmp_path):
    os.chdir(tmp_path)
    tmp_path.joinpath('foo.py').write_text(FOO_CONTENT)
    sys.path.insert(0, str(tmp_path))
    tmp_path.joinpath('pyproject.toml').write_text(TOML_CONTENT, encoding='utf-8')
    with patch('jupyter_packaging.build_api.orig_build_sdist') as orig_sdist:
        build_sdist(tmp_path)
        orig_sdist.assert_called_with(tmp_path, config_settings=None)
        data = tmp_path.joinpath('foo.txt').read_text(encoding='utf-8')
        assert data == 'fizz=buzz'


def test_build_sdist_bad_metadata(tmp_path):
    os.chdir(tmp_path)
    os.chdir(tmp_path)
    tmp_path.joinpath('foo.py').write_text(FOO_CONTENT)
    sys.path.insert(0, str(tmp_path))
    tmp_path.joinpath('pyproject.toml').write_text(BAD_CONTENT, encoding='utf-8')
    with patch('jupyter_packaging.build_api.orig_build_sdist') as orig_sdist:
        with pytest.raises(ValueError):
            build_sdist(tmp_path)
        orig_sdist.assert_not_called()


def test_build_sdist_no_toml(tmp_path):
    os.chdir(tmp_path)
    with patch('jupyter_packaging.build_api.orig_build_sdist') as orig_sdist:
        build_sdist(tmp_path)
        orig_sdist.assert_called_with(tmp_path, config_settings=None)
