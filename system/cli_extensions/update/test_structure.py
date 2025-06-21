# tests/test_structure.py
import os
import pytest

REQUIRED_DIRS = [
    "slick/core",
    "slick/services",
    "slick/interfaces",
    "tests/integration"
]

REQUIRED_FILES = [
    "slick/core/controller.py",
    "slick/services/version_control.py",
    "scripts/update_system.py"
]

@pytest.mark.parametrize("directory", REQUIRED_DIRS)
def test_directory_structure(directory):
    assert os.path.isdir(directory), f"Missing directory: {directory}"

@pytest.mark.parametrize("file", REQUIRED_FILES)
def test_required_files(file):
    assert os.path.isfile(file), f"Missing file: {file}"
    