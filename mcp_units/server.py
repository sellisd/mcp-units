#!/usr/bin/env python3

import asyncio
import json
import sys
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import EmbeddedResource, ImageContent, TextContent, Tool

from mcp_units.converters.temperature import convert_temperature
from mcp_units.converters.volume import VOLUME_RATIOS, convert_volume
from mcp_units.converters.weight import WEIGHT_RATIOS, convert_weight

__version__ = "0.2.0"


class ConversionTools(str, Enum):
    CONVERT_TEMPERATURE = "convert_temperature"
    CONVERT_VOLUME = "convert_volume"
    CONVERT_WEIGHT = "convert_weight"


# Schema definitions
TEMPERATURE_SCHEMA = {
    "type": "object",
    "properties": {
        "value": {"type": "number", "description": "Temperature value to convert"},
        "from_unit": {
            "type": "string",
            "enum": ["C", "F"],
            "description": "Source temperature unit (C or F)",
        },
        "to_unit": {
            "type": "string",
            "enum": ["C", "F"],
            "description": "Target temperature unit (C or F)",
        },
    },
    "required": ["value", "from_unit", "to_unit"],
}

VOLUME_SCHEMA = {
    "type": "object",
    "properties": {
        "value": {"type": "number", "description": "Volume value to convert"},
        "from_unit": {
            "type": "string",
            "enum": list(VOLUME_RATIOS.keys()),
            "description": "Source volume unit (ml, l, cup, tbsp, tsp)",
        },
        "to_unit": {
            "type": "string",
            "enum": list(VOLUME_RATIOS.keys()),
            "description": "Target volume unit (ml, l, cup, tbsp, tsp)",
        },
    },
    "required": ["value", "from_unit", "to_unit"],
}

WEIGHT_SCHEMA = {
    "type": "object",
    "properties": {
        "value": {"type": "number", "description": "Weight value to convert"},
        "from_unit": {
            "type": "string",
            "enum": list(WEIGHT_RATIOS.keys()),
            "description": "Source weight unit (g, kg, oz, lb)",
        },
        "to_unit": {
            "type": "string",
            "enum": list(WEIGHT_RATIOS.keys()),
            "description": "Target weight unit (g, kg, oz, lb)",
        },
    },
    "required": ["value", "from_unit", "to_unit"],
}


class ConversionResult:
    def __init__(self, value: Decimal, from_unit: str, to_unit: str):
        self.value = float(value)  # Convert Decimal to float for JSON serialization
        self.from_unit = from_unit
        self.to_unit = to_unit

    def model_dump(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "from_unit": self.from_unit,
            "to_unit": self.to_unit,
        }


class CookingUnitsServer:
    """Server implementation for cooking unit conversions."""

    def convert(
        self, conversion_type: ConversionTools, args: Dict[str, Any]
    ) -> ConversionResult:
        """Handle conversion requests for all unit types."""
        try:
            value = args["value"]
            from_unit = args["from_unit"]
            to_unit = args["to_unit"]

            if conversion_type == ConversionTools.CONVERT_TEMPERATURE:
                result = convert_temperature(value, from_unit, to_unit)
            elif conversion_type == ConversionTools.CONVERT_VOLUME:
                result = convert_volume(value, from_unit, to_unit)
            elif conversion_type == ConversionTools.CONVERT_WEIGHT:
                result = convert_weight(value, from_unit, to_unit)
            else:
                raise McpError(f"Unknown conversion type: {conversion_type}")

            return ConversionResult(result, from_unit, to_unit)

        except (ValueError, KeyError) as e:
            raise McpError(f"Conversion error: {str(e)}")
        except Exception as e:
            raise McpError(f"Unexpected error: {str(e)}")


async def serve() -> None:
    """Entry point for the MCP units server."""
    server = Server("mcp-units")
    units_server = CookingUnitsServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available conversion tools."""
        return [
            Tool(
                name=ConversionTools.CONVERT_TEMPERATURE.value,
                description="Convert between Celsius (C) and Fahrenheit (F) temperatures",
                inputSchema=TEMPERATURE_SCHEMA,
            ),
            Tool(
                name=ConversionTools.CONVERT_VOLUME.value,
                description="Convert between volume units (ml, l, cup, tbsp, tsp)",
                inputSchema=VOLUME_SCHEMA,
            ),
            Tool(
                name=ConversionTools.CONVERT_WEIGHT.value,
                description="Convert between weight units (g, kg, oz, lb)",
                inputSchema=WEIGHT_SCHEMA,
            ),
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls for unit conversions."""
        try:
            # Validate tool name
            try:
                tool = ConversionTools(name)
            except ValueError:
                raise ValueError(f"Unknown tool: {name}")

            # Perform conversion
            result = units_server.convert(tool, arguments)

            # Return formatted result
            return [
                TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))
            ]

        except Exception as e:
            raise ValueError(f"Error processing conversion request: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)


def main():
    """Start the MCP units server."""
    print("Starting MCP Units Server...", file=sys.stderr)
    try:
        asyncio.run(serve())
    except Exception as e:
        print(f"Server error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
