from decimal import Decimal, ROUND_HALF_UP
from typing import Union


def validate_temperature_unit(unit: str) -> bool:
    """Validate if the given unit is supported for temperature conversion."""
    return unit in ["C", "F"]


def convert_temperature(
    value: Union[int, float, str], from_unit: str, to_unit: str
) -> Decimal:
    """
    Convert a temperature measurement from one unit to another.

    Args:
        value: The temperature value to convert
        from_unit: The source unit (C or F)
        to_unit: The target unit (C or F)

    Returns:
        Decimal: The converted value rounded to 4 decimal places

    Raises:
        ValueError: If units are invalid or value format is incorrect
    """
    if not validate_temperature_unit(from_unit):
        raise ValueError(f"Invalid source unit: {from_unit}")
    if not validate_temperature_unit(to_unit):
        raise ValueError(f"Invalid target unit: {to_unit}")

    try:
        value_decimal = Decimal(str(value))
    except:
        raise ValueError(f"Invalid value: {value}")

    # Same unit, no conversion needed
    if from_unit == to_unit:
        return value_decimal.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

    # Convert to Celsius if needed
    if from_unit == "F":
        # °C = (°F - 32) × 5/9
        value_decimal = (value_decimal - Decimal("32")) * Decimal("5") / Decimal("9")

    # Convert to Fahrenheit if needed
    if to_unit == "F":
        # °F = (°C × 9/5) + 32
        value_decimal = (value_decimal * Decimal("9") / Decimal("5")) + Decimal("32")

    return value_decimal.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


# Common cooking temperatures in Celsius
COOKING_TEMPERATURES = {
    "water_boiling": Decimal("100.0"),
    "water_simmering": Decimal("85.0"),
    "deep_frying": Decimal("175.0"),  # Typical range: 175-190°C
    "baking_bread": Decimal("200.0"),
    "roasting": Decimal("180.0"),  # Typical range: 160-180°C
    "slow_cooking": Decimal("120.0"),
    "proofing": Decimal("35.0"),
}
