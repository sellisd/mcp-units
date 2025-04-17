import pytest
from decimal import Decimal
from src.converters.temperature import convert_temperature


def test_celsius_to_fahrenheit():
    """Test converting from Celsius to Fahrenheit."""
    # Water boiling point
    assert convert_temperature(100, "C", "F") == Decimal("212.0000")
    # Water freezing point
    assert convert_temperature(0, "C", "F") == Decimal("32.0000")
    # Room temperature
    assert convert_temperature(20, "C", "F") == Decimal("68.0000")
    # Baking temperature
    assert convert_temperature(180, "C", "F") == Decimal("356.0000")
    # Freezer temperature
    assert convert_temperature(-18, "C", "F") == Decimal("-0.4000")


def test_fahrenheit_to_celsius():
    """Test converting from Fahrenheit to Celsius."""
    # Water boiling point
    assert convert_temperature(212, "F", "C") == Decimal("100.0000")
    # Water freezing point
    assert convert_temperature(32, "F", "C") == Decimal("0.0000")
    # Room temperature
    assert convert_temperature(68, "F", "C") == Decimal("20.0000")
    # Baking temperature
    assert convert_temperature(350, "F", "C") == Decimal("176.6667")
    # Freezer temperature
    assert convert_temperature(0, "F", "C") == Decimal("-17.7778")


def test_common_cooking_temperatures():
    """Test common cooking temperature conversions."""
    # Deep frying
    assert convert_temperature(375, "F", "C") == Decimal("190.5556")
    assert convert_temperature(185, "C", "F") == Decimal("365.0000")

    # Slow cooking
    assert convert_temperature(250, "F", "C") == Decimal("121.1111")
    assert convert_temperature(120, "C", "F") == Decimal("248.0000")

    # Proofing dough
    assert convert_temperature(95, "F", "C") == Decimal("35.0000")
    assert convert_temperature(35, "C", "F") == Decimal("95.0000")


def test_same_unit_conversion():
    """Test converting between the same unit returns the same value."""
    assert convert_temperature(100, "C", "C") == Decimal("100.0000")
    assert convert_temperature(212, "F", "F") == Decimal("212.0000")
    assert convert_temperature(-40, "C", "C") == Decimal("-40.0000")


def test_invalid_units():
    """Test error handling for invalid units."""
    with pytest.raises(ValueError, match="Invalid source unit: K"):
        convert_temperature(100, "K", "C")

    with pytest.raises(ValueError, match="Invalid target unit: R"):
        convert_temperature(100, "C", "R")


def test_invalid_values():
    """Test error handling for invalid values."""
    with pytest.raises(ValueError, match="Invalid value: abc"):
        convert_temperature("abc", "C", "F")

    with pytest.raises(ValueError, match="Invalid value: None"):
        convert_temperature(None, "F", "C")
