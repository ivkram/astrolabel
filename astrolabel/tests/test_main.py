from astrolabel import AstroLabels
from astrolabel.main import DEFAULT_LIBRARY_PATH
import pytest

import os
import shutil


@pytest.fixture(scope="module")
def al() -> AstroLabels:
    al = AstroLabels.read()
    assert al.library_fname() == DEFAULT_LIBRARY_PATH

    return al


@pytest.fixture
def tmp_library_path(tmp_path):
    library_path = tmp_path / "astrolabel.yml"
    shutil.copy(DEFAULT_LIBRARY_PATH, library_path)

    return library_path


def test_read_from_file(tmp_library_path):
    al = AstroLabels.read(tmp_library_path)

    assert al.library_fname() == tmp_library_path


def test_read_from_env_variable(tmp_library_path, monkeypatch):
    monkeypatch.setenv("ASTROLABEL", str(tmp_library_path))
    al = AstroLabels.read()

    assert al.library_fname() == tmp_library_path


def test_read_from_workdir(tmp_library_path, monkeypatch):
    monkeypatch.chdir(tmp_library_path.parent)
    al = AstroLabels.read()

    assert al.library_fname() == tmp_library_path


def test_read_not_found():
    with pytest.raises(FileNotFoundError, match="The file \".*\" does not exist"):
        AstroLabels.read("non_existing_file.yml")


def test_without_unit(al):
    assert al.get_label('z') == '$z$'


def test_with_unit(al):
    assert al.get_label('sfr') == r'$\mathrm{SFR}$ [$\mathrm{M_{\odot}\,yr^{-1}}$]'


def test_log_without_unit(al):
    assert al.get_label('z', fmt='log') == r'$\log_{10}\,\left(z\right)$'


def test_log_with_unit(al):
    assert al.get_label('sfr', fmt='log') == (r'$\log_{10}\,\left(\mathrm{SFR} / \left(\mathrm{M_{\odot}\,'
                                              r'yr^{-1}}\right)\right)$')
