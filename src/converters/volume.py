from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Union

# Conversion ratios normalized to milliliters
# Using exact ratios for common kitchen conversions
VOLUME_RATIOS: Dict[str, Decimal] = {
    "ml": Decimal("1.0"),
    "l": Decimal("1000.0"),
    "cup": Decimal("236.5882365"),  # Precise US cup
    "tbsp": Decimal("14.7867647875"),  # Cup/16 for exact tablespoon conversion
    "tsp": Decimal("4.92892159583")  # Tablespoon/3 for exact teaspoon conversion
}

def validate_volume_unit(unit: str) -> bool:
    """Validate if the given unit is supported for volume conversion."""
    return unit in VOLUME_RATIOS

def convert_volume(value: Union[int, float, str], from_unit: str, to_unit: str) -> Decimal:
    """
    Convert a volume measurement from one unit to another.
    
    Args:
        value: The value to convert
        from_unit: The source unit (ml, l, cup, tbsp, tsp)
        to_unit: The target unit (ml, l, cup, tbsp, tsp)
    
    Returns:
        Decimal: The converted value rounded to 4 decimal places
    
    Raises:
        ValueError: If units are invalid or value is negative
    """
    if not validate_volume_unit(from_unit):
        raise ValueError(f"Invalid source unit: {from_unit}")
    if not validate_volume_unit(to_unit):
        raise ValueError(f"Invalid target unit: {to_unit}")

    try:
        value_decimal = Decimal(str(value))
    except:
        raise ValueError(f"Invalid value: {value}")

    if value_decimal < 0:
        raise ValueError("Value cannot be negative")

    # Convert to base unit (ml)
    base_value = value_decimal * VOLUME_RATIOS[from_unit]
    
    # Convert from base unit to target unit
    result = base_value / VOLUME_RATIOS[to_unit]
    
    # Round to 4 decimal places
    return result.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)