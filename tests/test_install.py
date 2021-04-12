import subprocess
import shutil
from pathlib import Path
import sysconfig


def test_install(make_package, tmp_path):
    name = 'jupyter_packaging_test_foo'
    package_dir = make_package(name=name)
    subprocess.check_output([shutil.which('pip'), 'install', '.'], cwd=str(package_dir))
    # Get site packages where the package is installed.
    sitepkg = Path(sysconfig.get_paths()["purelib"])
    installed_file = sitepkg / f"{name}/main.py"
    assert installed_file.exists()
    excluded_file = sitepkg / f"{name}/exclude.py"
    assert not excluded_file.exists()
    subprocess.check_output([shutil.which('pip'), 'uninstall', name, '-y'], cwd=str(package_dir))
    assert not installed_file.exists()


def test_install_hybrid(make_hybrid_package, tmp_path):
    name = 'jupyter_packaging_test_foo'
    package_dir = make_hybrid_package(name=name)
    subprocess.check_output([shutil.which('pip'), 'install', '.'], cwd=str(package_dir))
    # Get site packages where the package is installed.
    sitepkg = Path(sysconfig.get_paths()["purelib"])
    installed_py_file = sitepkg / f"{name}/main.py"
    installed_js_file = sitepkg / f"{name}/generated.js"
    assert installed_py_file.exists()
    assert installed_js_file.exists()
    excluded_file = sitepkg / f"{name}/exclude.py"
    assert not excluded_file.exists()
    subprocess.check_output([shutil.which('pip'), 'uninstall', name, '-y'], cwd=str(package_dir))
    assert not installed_py_file.exists()
    assert not installed_js_file.exists()
