import pytest
from decimal import Decimal
from src.converters import convert_volume, convert_weight

def test_volume_conversions():
    """Test various volume conversions"""
    # Test ml to other units
    assert convert_volume(1000, "ml", "l") == Decimal("1.0000")
    assert convert_volume(236.5882365, "ml", "cup") == Decimal("1.0000")
    assert convert_volume(14.7867647875, "ml", "tbsp") == Decimal("1.0000")
    assert convert_volume(4.92892159583, "ml", "tsp") == Decimal("1.0000")

    # Test cup to other units
    assert convert_volume(1, "cup", "ml") == Decimal("236.5882")
    assert convert_volume(1, "cup", "tbsp") == Decimal("16.0000")
    assert convert_volume(1, "cup", "tsp") == Decimal("48.0000")

    # Test tablespoon to teaspoon
    assert convert_volume(1, "tbsp", "tsp") == Decimal("3.0000")

    # Test common kitchen equivalences
    assert convert_volume(1, "cup", "tbsp") == Decimal("16.0000")  # 1 cup = 16 tbsp
    assert convert_volume(1, "tbsp", "tsp") == Decimal("3.0000")   # 1 tbsp = 3 tsp
    assert convert_volume(1, "cup", "tsp") == Decimal("48.0000")   # 1 cup = 48 tsp

def test_weight_conversions():
    """Test various weight conversions"""
    # Test g to other units
    assert convert_weight(1000, "g", "kg") == Decimal("1.0000")
    assert convert_weight(28.3495, "g", "oz") == Decimal("1.0000")
    assert convert_weight(453.592, "g", "lb") == Decimal("1.0000")

    # Test pounds to other units
    assert convert_weight(1, "lb", "oz") == Decimal("16.0000")
    assert convert_weight(1, "lb", "g") == Decimal("453.5920")

    # Test kilograms to other units
    assert convert_weight(1, "kg", "g") == Decimal("1000.0000")
    assert convert_weight(1, "kg", "lb") == Decimal("2.2046")

def test_invalid_inputs():
    """Test error handling for invalid inputs"""
    # Test invalid units
    with pytest.raises(ValueError):
        convert_volume(1, "invalid", "ml")
    with pytest.raises(ValueError):
        convert_weight(1, "g", "invalid")

    # Test negative values
    with pytest.raises(ValueError):
        convert_volume(-1, "ml", "l")
    with pytest.raises(ValueError):
        convert_weight(-1, "g", "kg")

    # Test invalid value types
    with pytest.raises(ValueError):
        convert_volume("invalid", "ml", "l")
    with pytest.raises(ValueError):
        convert_weight("invalid", "g", "kg")

def test_roundtrip_conversions():
    """Test that converting back and forth preserves values (within rounding)"""
    # Volume roundtrip
    original_volume = Decimal("5.5")
    converted = convert_volume(
        convert_volume(original_volume, "cup", "ml"),
        "ml", "cup"
    )
    assert abs(converted - original_volume) < Decimal("0.0001")

    # Weight roundtrip
    original_weight = Decimal("10.5")
    converted = convert_weight(
        convert_weight(original_weight, "lb", "g"),
        "g", "lb"
    )
    assert abs(converted - original_weight) < Decimal("0.0001")