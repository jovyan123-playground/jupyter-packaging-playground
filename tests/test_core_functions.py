import os

import pytest
from unittest.mock import patch, call

from jupyter_packaging.setupbase import npm_builder, wrap_installers


def test_wrap_installers():
    called = False
    def func():
        nonlocal called
        called = True

    cmd_class = wrap_installers(func)
    cmd_class['pre_sdist'](Distribution()).run()
    assert called


def test_npm_builder():
    with patch('jupyter_packaging.setupbase.which') as which, patch('jupyter_packaging.setupbase.run') as run:
        builder = npm_builder()
        which.return_value = ['foo']
        builder()
        cwd=os.getcwd()
        run.assert_has_calls([
            call(['npm', 'install'], cwd=cwd),
            call(['npm', 'run', 'build'], cwd=cwd)
        ])


def test_npm_build_skip():
    with patch('jupyter_packaging.setupbase.which') as which, patch('jupyter_packaging.setupbase.run') as run, patch('jupyter_packaging.setupbase.skip_npm', True):
        builder = npm_builder()
        which.return_value = ['foo']
        builder()
        run.assert_not_called()


def test_npm_builder_yarn(tmp_path):
    with patch('jupyter_packaging.setupbase.which') as which, patch('jupyter_packaging.setupbase.run') as run:
        tmp_path.joinpath('yarn.lock').write_text('hello')
        builder = npm_builder(path=tmp_path)
        which.return_value = ['foo']
        builder()
        cwd=os.getcwd()
        run.assert_has_calls([
            call(['yarn', 'install'], cwd=tmp_path),
            call(['yarn', 'run', 'build'], cwd=tmp_path)
        ])


def test_npm_builder_not_stale(tmp_path):
    with patch('jupyter_packaging.setupbase.which') as which, patch('jupyter_packaging.setupbase.run') as run, patch('jupyter_packaging.setupbase.is_stale') as is_stale:
        is_stale.return_value = False
        builder = npm_builder(build_dir=tmp_path, source_dir=tmp_path)
        which.return_value = ['foo']
        builder()
        run.assert_not_called()


def test_npm_builder_no_npm():
    with patch('jupyter_packaging.setupbase.which') as which, patch('jupyter_packaging.setupbase.run') as run, patch('jupyter_packaging.setupbase.is_stale') as is_stale:
        is_stale.return_value = False
        builder = npm_builder()
        which.return_value = []
        builder()
        run.assert_not_called()
