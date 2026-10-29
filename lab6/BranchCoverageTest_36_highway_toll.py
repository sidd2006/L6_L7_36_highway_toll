"""Tests targeting both outcomes of each decision in highway_toll.py."""
import pytest
from highway_toll import toll_for, toll_charge, pass_advice


@pytest.mark.parametrize("axles", [1, 0, -2])
def test_invalid_axle_branch(axles):
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(axles, False, False)


@pytest.mark.parametrize("axles,expected", [(2, 100), (3, 150), (4, 250), (6, 400)])
def test_known_and_fallback_axle_branches(axles, expected):
    assert toll_for(axles, False, False) == expected


def test_peak_true_and_false_branches():
    assert toll_for(2, True, False) == 125
    assert toll_for(2, False, False) == 100


def test_fastag_true_two_axle_and_non_two_axle_branches():
    assert toll_for(2, False, True) == 90
    assert toll_for(3, False, True) == 142.5


def test_exempt_and_non_exempt_vehicle_branches():
    assert toll_charge("ambulance", 2, False, False) == 0
    assert toll_charge("fire_engine", 3, True, True) == 0
    assert toll_charge("car", 2, False, False) == 100


def test_pass_advice_all_outcomes():
    assert pass_advice([(False, False), (False, False)], 2, 150) == "buy_pass"
    assert pass_advice([(False, False)], 2, 100) == "either"
    assert pass_advice([(False, False)], 2, 150) == "pay_per_trip"


def test_pass_advice_loop_not_entered():
    assert pass_advice([], 2, 0) == "either"
