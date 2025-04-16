from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional
from jsonschema import validate, ValidationError

# Common schema components
NUMBER_SCHEMA = {
    "type": "number",
    "minimum": 0
}

# Volume conversion schema
VOLUME_CONVERSION_SCHEMA = {
    "type": "object",
    "properties": {
        "value": NUMBER_SCHEMA,
        "from_unit": {
            "type": "string",
            "enum": ["ml", "l", "cup", "tbsp", "tsp"]
        },
        "to_unit": {
            "type": "string",
            "enum": ["ml", "l", "cup", "tbsp", "tsp"]
        }
    },
    "required": ["value", "from_unit", "to_unit"],
    "additionalProperties": False
}

# Weight conversion schema
WEIGHT_CONVERSION_SCHEMA = {
    "type": "object",
    "properties": {
        "value": NUMBER_SCHEMA,
        "from_unit": {
            "type": "string",
            "enum": ["g", "kg", "oz", "lb"]
        },
        "to_unit": {
            "type": "string",
            "enum": ["g", "kg", "oz", "lb"]
        }
    },
    "required": ["value", "from_unit", "to_unit"],
    "additionalProperties": False
}

def validate_conversion_request(data: Dict[str, Any], schema: Dict[str, Any]) -> Optional[str]:
    """
    Validate a conversion request against a schema.
    
    Args:
        data: The request data to validate
        schema: The JSON schema to validate against
    
    Returns:
        Optional[str]: Error message if validation fails, None if validation succeeds
    """
    try:
        validate(instance=data, schema=schema)
        
        # Additional validation for value type
        try:
            value = Decimal(str(data["value"]))
            if value < 0:
                return "Value cannot be negative"
        except (InvalidOperation, TypeError):
            return f"Invalid value format: {data['value']}"
            
        return None
    except ValidationError as e:
        return f"Validation error: {e.message}"

def format_error_response(message: str) -> Dict[str, Any]:
    """Format an error response according to MCP protocol."""
    return {
        "content": [
            {
                "type": "text",
                "text": message
            }
        ],
        "isError": True
    }

def format_success_response(value: Decimal, unit: str) -> Dict[str, Any]:
    """Format a successful conversion response according to MCP protocol."""
    return {
        "content": [
            {
                "type": "text",
                "text": f"{value} {unit}"
            }
        ],
        "isError": False
    }