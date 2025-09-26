from decimal import Decimal, InvalidOperation
from typing import Any, Dict

from jsonschema import ValidationError, validate
from mcp import McpError

# Common schema components
NUMBER_SCHEMA = {"type": "number", "minimum": 0}

# Schema for temperatures that can be negative
TEMPERATURE_NUMBER_SCHEMA = {"type": "number"}

# Volume conversion schema
VOLUME_CONVERSION_SCHEMA = {
    "type": "object",
    "properties": {
        "value": NUMBER_SCHEMA,
        "from_unit": {"type": "string", "enum": ["ml", "l", "cup", "tbsp", "tsp"]},
        "to_unit": {"type": "string", "enum": ["ml", "l", "cup", "tbsp", "tsp"]},
    },
    "required": ["value", "from_unit", "to_unit"],
    "additionalProperties": False,
}

# Weight conversion schema
WEIGHT_CONVERSION_SCHEMA = {
    "type": "object",
    "properties": {
        "value": NUMBER_SCHEMA,
        "from_unit": {"type": "string", "enum": ["g", "kg", "oz", "lb"]},
        "to_unit": {"type": "string", "enum": ["g", "kg", "oz", "lb"]},
    },
    "required": ["value", "from_unit", "to_unit"],
    "additionalProperties": False,
}

# Temperature conversion schema
TEMPERATURE_CONVERSION_SCHEMA = {
    "type": "object",
    "properties": {
        "value": TEMPERATURE_NUMBER_SCHEMA,
        "from_unit": {"type": "string", "enum": ["C", "F"]},
        "to_unit": {"type": "string", "enum": ["C", "F"]},
    },
    "required": ["value", "from_unit", "to_unit"],
    "additionalProperties": False,
}

def validate_conversion_request(data: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """
    Validate a conversion request against a schema.

    Args:
        data: The request data to validate
        schema: The JSON schema to validate against

    Raises:
        MCPError: If validation fails
    """
    try:
        validate(instance=data, schema=schema)

        # Additional validation for value type
        try:
            value = Decimal(str(data["value"]))
            # Only check for negative values on non-temperature conversions
            if schema != TEMPERATURE_CONVERSION_SCHEMA and value < 0:
                raise McpError("Value cannot be negative")
        except (InvalidOperation, TypeError):
            raise McpError(f"Invalid value format: {data['value']}")

    except ValidationError as e:
        raise McpError(f"Validation error: {e.message}")
