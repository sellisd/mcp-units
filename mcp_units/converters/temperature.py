from decimal import ROUND_HALF_UP, Decimal


def validate_temperature_unit(unit: str) -> bool:
    """Validate if the given unit is supported for temperature conversion."""
    return unit in ["C", "F"]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> Decimal:
    """
    Convert temperature between Celsius and Fahrenheit with precise decimal handling.

    Args:
        value: Temperature value to convert
        from_unit: Source unit (C or F)
        to_unit: Target unit (C or F)

    Returns:
        Decimal: Converted temperature value rounded to 4 decimal places

    Raises:
        ValueError: If conversion fails or input is invalid
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
