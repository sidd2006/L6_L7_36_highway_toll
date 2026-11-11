"""Validate highway toll inputs and demonstrate each calculation."""

import re


PLATE_PATTERN = re.compile(r"([A-Za-z]{2})-([0-9]{2})-[A-Za-z]{1,3}-([0-9]{4})")
TRIP_PATTERN = re.compile(r"([0-9]+)\s*[xX]\s*([0-9]+)")
AXLE_PATTERN = re.compile(r"\+?[0-9]+")


def parse_plate(plate):
    """Return the uppercase state, district number, and registration number."""
    match = PLATE_PATTERN.fullmatch(plate.strip()) if isinstance(plate, str) else None
    if match is None:
        raise ValueError("expected a plate like KA-05-AB-1234")
    state, district, number = match.groups()
    return state.upper(), int(district), int(number)


def trip_cost(text):
    """Multiply a nonnegative whole-number trip count and rate."""
    match = TRIP_PATTERN.fullmatch(text.strip()) if isinstance(text, str) else None
    if match is None:
        raise ValueError("expected nonnegative whole numbers in the form 3x150")
    count, rate = match.groups()
    return int(count) * int(rate)


def axle_class(axles):
    """Classify a vehicle with at least two axles."""
    if isinstance(axles, str) and AXLE_PATTERN.fullmatch(axles.strip()):
        axles = int(axles)
    if isinstance(axles, bool) or not isinstance(axles, int) or axles < 2:
        raise ValueError("expected a whole axle count of at least 2")
    if axles == 2:
        return "car"
    if axles <= 4:
        return "truck"
    return "heavy"


def main():
    steps = (
        (parse_plate, "Enter a plate (e.g. KA-05-AB-1234): ", "State, District and Number"),
        (trip_cost, "Enter trips x rate (e.g. 3x150): ", "Trip Cost"),
        (axle_class, "Enter an axle count (e.g. 3): ", "Vehicle Class"),
    )
    for index, (calculate, prompt, label) in enumerate(steps):
        if index:
            print()
        print(f"==== Running {calculate.__name__} ====")
        try:
            value = input(prompt)
        except EOFError:
            print("\nInput ended.")
            return
        try:
            print(f"{label}: {calculate(value)}")
        except ValueError as error:
            print(f"Invalid input: {error}.")


if __name__ == "__main__":
    main()
