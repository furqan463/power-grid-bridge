# SPDX-FileCopyrightText: 2026 Engr. Ahmad Furqan <ahmadfurqanc@gmail.com>
#
# SPDX-License-Identifier: MPL-2.0

import importlib.util
from pathlib import Path

from setuptools import setup


def prepare_pkg(setup_file: Path):
    pkg_dir = setup_file.parent

    # Dynamically import and trigger set_pypi_version.py calculations
    # to guarantee fresh validation whether running locally or on CI/CD
    script_path = pkg_dir / "set_pypi_version.py"
    if script_path.exists():
        spec = importlib.util.spec_from_file_location("set_pypi_version", script_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.set_version(pkg_dir)
    else:
        # Minimal fallback if running isolated builds without the script file
        pypi_file = pkg_dir / "PYPI_VERSION"
        if not pypi_file.exists():
            version_source = pkg_dir / "VERSION"
            version = version_source.read_text().strip() if version_source.exists() else "0.1.0"
            pypi_file.write_text(version)

prepare_pkg(Path(__file__).resolve())
setup()
