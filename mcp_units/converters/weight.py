from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Union

# Conversion ratios normalized to grams
WEIGHT_RATIOS: Dict[str, Decimal] = {
    "g": Decimal("1.0"),
    "kg": Decimal("1000.0"),
    "oz": Decimal("28.3495"),
    "lb": Decimal("453.592"),
}


def validate_weight_unit(unit: str) -> bool:
    """Validate if the given unit is supported for weight conversion."""
    return unit in WEIGHT_RATIOS


def convert_weight(
    value: Union[int, float, str], from_unit: str, to_unit: str
) -> Decimal:
    """
    Convert a weight measurement from one unit to another.

    Args:
        value: The value to convert
        from_unit: The source unit (g, kg, oz, lb)
        to_unit: The target unit (g, kg, oz, lb)

    Returns:
        Decimal: The converted value rounded to 4 decimal places

    Raises:
        ValueError: If units are invalid or value is negative
    """
    if not validate_weight_unit(from_unit):
        raise ValueError(f"Invalid source unit: {from_unit}")
    if not validate_weight_unit(to_unit):
        raise ValueError(f"Invalid target unit: {to_unit}")

    try:
        value_decimal = Decimal(str(value))
    except:
        raise ValueError(f"Invalid value: {value}")

    if value_decimal < 0:
        raise ValueError("Value cannot be negative")

    # Convert to base unit (g)
    base_value = value_decimal * WEIGHT_RATIOS[from_unit]

    # Convert from base unit to target unit
    result = base_value / WEIGHT_RATIOS[to_unit]

    # Round to 4 decimal places
    return result.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
