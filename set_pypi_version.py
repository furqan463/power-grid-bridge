# SPDX-FileCopyrightText: 2026 Engr. Ahmad Furqan <ahmadfurqanc@gmail.com>
#
# SPDX-License-Identifier: MPL-2.0

import os
import sys
from pathlib import Path

import requests

# Define your package name as registered on PyPI
PYPI_PACKAGE_NAME = "power-grid-bridge"

def set_version(pkg_dir: Path):
    version_file = pkg_dir / "VERSION"
    if not version_file.exists():
        print(f"Error: {version_file} file not found. Creating a default '0.1' file.", file=sys.stderr)
        with version_file.open("w") as f:
            f.write("0.1\n")

    with version_file.open() as f:
        version = f.read().strip().strip("\n")

    # Safely parse major.minor from your target config (e.g., "0.1")
    version_parts = [int(x) for x in version.split(".")]
    major = version_parts[0]
    minor = version_parts[1] if len(version_parts) > 1 else 0

    # Fetch latest from PyPI
    latest_major, latest_minor, latest_patch = get_pypi_latest()

    # Calculate new version
    version = get_new_version(major, minor, latest_major, latest_minor, latest_patch)

    # Mutate version in GitHub Actions if running in CI
    if ("GITHUB_SHA" in os.environ) and ("GITHUB_REF" in os.environ) and ("GITHUB_RUN_NUMBER" in os.environ):
        sha = os.environ["GITHUB_SHA"]
        ref = os.environ["GITHUB_REF"]
        build_number = os.environ["GITHUB_RUN_NUMBER"]
        # Convert short hash to numeric string
        short_hash = f"{int(f'0x{sha[0:6]}', base=16):08}"

        if "main" in ref or "master" in ref:
            # Main branch uses standard release tracking
            pass
        else:
            # Feature branch gets alpha tag format: major.minor.patcha1<build><hash>
            version += f"a1{build_number}{short_hash}"

    print(f"Setting target PyPI distribution version to: {version}")
    with (pkg_dir / "PYPI_VERSION").open("w") as f:
        f.write(version)


def get_pypi_latest():
    """Fetches the latest release version from PyPI. Returns (0, 0, 0) if package doesn't exist yet."""
    try:
        request = requests.get(f"https://pypi.org/pypi/{PYPI_PACKAGE_NAME}/json", timeout=10)
        if request.status_code == 404:  # noqa: PLR2004
            # Package has never been published before
            return 0, 1, 0

        request.raise_for_status()
        data = request.json()
        version_str = str(data["info"]["version"])

        # Parse standard 3-part version
        parts = [int(x) for x in version_str.split(".")]
        while len(parts) < 3:  # noqa: PLR2004
            parts.append(0)
        return parts[0], parts[1], parts[2]

    except Exception as e:  # noqa: BLE001
        print(f"Warning: Could not fetch from PyPI ({e}). Defaulting baseline to 0.0.0", file=sys.stderr)
        return 0, 1, 0


def get_new_version(major, minor, latest_major, latest_minor, latest_patch):
    if (major > latest_major) or ((major == latest_major) and minor > latest_minor):
        # Brand-new version target, reset patch count to 0
        return f"{major}.{minor}.0"

    if major == latest_major and minor == latest_minor:
        # Appending an incremental fix/patch onto the existing live version
        return f"{major}.{minor}.{latest_patch + 1}"

    # Anti-downgrade guardrail
    raise ValueError(
        "Invalid version number target!\n"
        f"Latest live PyPI version: {latest_major}.{latest_minor}.{latest_patch}\n"
        f"Your local VERSION config dictates: {major}.{minor}\n"
        "Please increment the values inside your 'VERSION' file."
    )


if __name__ == "__main__":
    set_version(Path(__file__).parent)
