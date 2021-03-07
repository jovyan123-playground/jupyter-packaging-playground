# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import functools
import importlib
from pathlib import Path

from setuptools.build_meta import (
    get_requires_for_build_wheel,
    get_requires_for_build_sdist,
    prepare_metadata_for_build_wheel,
    build_sdist as orig_build_sdist,
    build_wheel as orig_build_wheel
)
import tomlkit


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """Build a wheel with an optional pre-build step."""
    builder = _get_build_func()
    if builder:
        builder()
    return orig_build_wheel(wheel_directory, config_settings=config_settings, metadata_directory=metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    """Build an sdist with an optional pre-build step."""
    builder = _get_build_func()
    if builder:
        builder()
    return orig_build_sdist(sdist_directory, config_settings=config_settings)


def _get_build_func():
    pyproject = Path('pyproject.toml')
    if not pyproject.exists():
        return
    data = tomlkit.loads(pyproject.read_text(encoding='utf-8'))
    if 'tool' not in data:
        return
    if 'jupyter-packaging' not in data['tool']:
        return
    if 'builder' not in data['tool']['jupyter-packaging']:
        return
    section = data['tool']['jupyter-packaging']
    if 'func' not in section['builder']:
        raise ValueError('Missing `func` specifier for builder')

    func_data = section['builder']['func']
    mod_name, _, func_name = func_data.rpartition('.')
    mod = importlib.import_module(mod_name)
    func = getattr(mod, func_name)
    kwargs = section.get('build-args', {})
    return functools.partial(func, **kwargs)
