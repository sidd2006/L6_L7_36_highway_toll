"""Tests aimed at achieving high line coverage for highway_toll.py."""
import pytest
from highway_toll import toll_for, toll_charge, pass_advice


def test_invalid_axle_count_raises_value_error():
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)


def test_known_axle_rates():
    assert toll_for(2, False, False) == 100
    assert toll_for(3, False, False) == 150
    assert toll_for(4, False, False) == 250


def test_unknown_axle_count_uses_default_rate():
    assert toll_for(5, False, False) == 400


def test_peak_hour_surcharge():
    assert toll_for(2, True, False) == 125


def test_fastag_discounts():
    assert toll_for(2, False, True) == 90
    assert toll_for(3, False, True) == 142.5


def test_peak_and_fastag_combined():
    assert toll_for(4, True, True) == 296.88


def test_exempt_vehicles():
    assert toll_charge("ambulance", 2, False, False) == 0
    assert toll_charge("fire_engine", 4, True, True) == 0


def test_non_exempt_vehicle_is_charged():
    assert toll_charge("car", 2, False, False) == 100


def test_pass_advice_buy_pass():
    assert pass_advice([(False, False), (False, False)], 2, 150) == "buy_pass"


def test_pass_advice_exact_price():
    assert pass_advice([(False, False)], 2, 100) == "either"


def test_pass_advice_pay_per_trip_and_empty_trips():
    assert pass_advice([(False, False)], 2, 150) == "pay_per_trip"
    assert pass_advice([], 2, 0) == "either"
