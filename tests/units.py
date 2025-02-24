"""Test units."""


# --- import -------------------------------------------------------------------------------------

import numpy as np
import pytest
import pint

import WrightTools as wt
from WrightTools import datasets


# --- test ---------------------------------------------------------------------------------------


def test_axis_convert_exception():
    p = datasets.PyCMDS.w2_w1_000
    data = wt.data.from_PyCMDS(p)
    try:
        data.w2.convert("fs")
    except wt.exceptions.UnitsError:
        assert True
    else:
        assert False


def test_in_mm_conversion():
    assert np.isclose(wt.units.convert(25.4, "mm", "in"), 1.0)
    assert np.isclose(wt.units.convert(1.0, "in", "mm"), 25.4)


def test_unit_registry():
    values = np.linspace(-1, 1, 51)
    d = wt.Data(name="test")
    d.create_variable("Bgood", values=values, units="tesla")
    d.transform("Bgood")


def test_bad_unit_registry():
    values = np.linspace(-1, 1, 51)
    d = wt.Data(name="test")
    with pytest.raises(ValueError):
        d.create_variable("Bbad", values=values, units="Tesla")
        d.transform("Bbad")


def test_0_inf():
    assert wt.units.convert(0, "wn", "nm") == np.inf
    assert wt.units.convert(0, "nm", "wn") == np.inf


def test_round_trip():
    start = 12500.0
    halftrip = wt.units.convert(start, "wn", "eV")
    fulltrip = wt.units.convert(halftrip, "eV", "wn")
    assert np.isclose(start, fulltrip)


def test_return_input_noerror():
    val = 12500
    out = wt.units.convert(val, current_unit=None, destination_unit=None)
    assert val == out


def test_return_input_warning():
    val = 12500
    with pytest.warns(UserWarning):
        out = wt.units.convert(val, None, "eV")
        assert val == out
    with pytest.warns(UserWarning):
        out = wt.units.convert(val, "wn", None)
        assert val == out


def test_error():
    val = 12500
    with pytest.raises(pint.errors.DimensionalityError):
        wt.units.convert(val, "wn", "W")
    with pytest.raises(pint.errors.DimensionalityError):
        wt.units.convert(val, "W", "wn")
