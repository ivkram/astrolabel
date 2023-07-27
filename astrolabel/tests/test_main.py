from astrolabel import AstroLabels
import pytest


@pytest.fixture(scope="module")
def al() -> AstroLabels:
    return AstroLabels.read()


def test_without_unit(al):
    assert al.get_label('z') == '$z$'


def test_with_unit(al):
    assert al.get_label('sfr') == r'$\mathrm{SFR}$ [$\mathrm{M_{\odot}\,yr^{-1}}$]'


def test_log_without_unit(al):
    assert al.get_label('z', fmt='log') == r'$\log_{10}\,\left(z\right)$'


def test_log_with_unit(al):
    assert al.get_label('sfr', fmt='log') == (r'$\log_{10}\,\left(\mathrm{SFR} / \left(\mathrm{M_{\odot}\,'
                                              r'yr^{-1}}\right)\right)$')
