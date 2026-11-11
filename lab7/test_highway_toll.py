"""Property-based tests for the three Lab 7 input formats."""

import string

import pytest
from hypothesis import given, strategies as st

from highway_toll import axle_class, parse_plate, trip_cost


LETTERS = string.ascii_letters
NON_TEXT = st.none() | st.booleans() | st.floats() | st.binary() | st.lists(st.integers())


@given(
    state=st.text(LETTERS, min_size=2, max_size=2),
    district=st.integers(0, 99),
    series=st.text(LETTERS, min_size=1, max_size=3),
    number=st.integers(0, 9999),
)
def test_parse_plate_extracts_fields(state, district, series, number):
    plate = f"{state}-{district:02d}-{series}-{number:04d}"
    assert parse_plate(plate) == (state.upper(), district, number)


@given(
    NON_TEXT
    | st.text(alphabet=string.digits)
    | st.integers(0, 99).map(lambda series: f"KA-05-{series}-1234")
    | st.integers(0, 999).map(lambda number: f"KA-05-AB-{number}")
)
def test_parse_plate_rejects_invalid_input(value):
    with pytest.raises(ValueError):
        parse_plate(value)


@given(count=st.integers(0), rate=st.integers(0), separator=st.sampled_from(["x", "X"]))
def test_trip_cost_multiplies_count_and_rate(count, rate, separator):
    assert trip_cost(f"{count} {separator} {rate}") == count * rate


@given(
    NON_TEXT
    | st.text(alphabet=string.digits)
    | st.integers(max_value=-1).map(lambda count: f"{count}x150")
    | st.integers(max_value=-1).map(lambda rate: f"3x{rate}")
    | st.integers(0).map(lambda count: f"{count}.5x150")
)
def test_trip_cost_rejects_invalid_input(value):
    with pytest.raises(ValueError):
        trip_cost(value)


@given(st.one_of(st.sampled_from([2, 3, 4, 5]), st.integers(min_value=2)))
def test_axle_class_categorizes_whole_counts(axles):
    expected = {2: "car", 3: "truck", 4: "truck"}.get(axles, "heavy")
    assert axle_class(axles) == expected
    assert axle_class(f" +{axles} ") == expected


@given(
    NON_TEXT
    | st.integers(max_value=1)
    | st.integers(max_value=1).map(str)
    | st.integers(2).map(lambda axles: f"{axles}.5")
)
def test_axle_class_rejects_invalid_input(value):
    with pytest.raises(ValueError):
        axle_class(value)
