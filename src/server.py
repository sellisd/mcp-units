#!/usr/bin/env python3

import sys
from typing import Dict, Any, List
from mcp import Tool, McpError, ServerCapabilities, ServerSession, Implementation, stdio_server

from src import __version__
from converters.volume import convert_volume
from converters.weight import convert_weight
from converters.temperature import convert_temperature
from utils.validation import (
    VOLUME_CONVERSION_SCHEMA,
    WEIGHT_CONVERSION_SCHEMA,
    TEMPERATURE_CONVERSION_SCHEMA,
)

class CookingUnitsServer(ServerSession):
    """MCP server for cooking unit conversions."""

    def __init__(self, read_stream, write_stream, init_options):
        super().__init__(read_stream, write_stream, init_options)
        self._implementation = Implementation(
            name="mcp-units",
            version=__version__,
            capabilities=ServerCapabilities()
        )
        self.register_tools()

    def register_tools(self) -> None:
        """Register conversion tools with the MCP server."""
        self._tools: List[Tool] = [
            Tool(
                name="convert_volume",
                description="Convert between volume measurements (ml, l, cup, tbsp, tsp)",
                inputSchema=VOLUME_CONVERSION_SCHEMA,
                handler=self.handle_volume_conversion,
                returns={"type": "number"}
            ),
            Tool(
                name="convert_weight",
                description="Convert between weight measurements (g, kg, oz, lb)",
                inputSchema=WEIGHT_CONVERSION_SCHEMA,
                handler=self.handle_weight_conversion,
                returns={"type": "number"}
            ),
            Tool(
                name="convert_temperature",
                description="Convert between cooking temperature units (C, F)",
                inputSchema=TEMPERATURE_CONVERSION_SCHEMA,
                handler=self.handle_temperature_conversion,
                returns={"type": "number"}
            )
        ]

    def handle_volume_conversion(self, args: Dict[str, Any]) -> Any:
        """Handle volume conversion requests."""
        try:
            return convert_volume(args["value"], args["from_unit"], args["to_unit"])
        except ValueError as e:
            raise McpError(str(e))

    def handle_weight_conversion(self, args: Dict[str, Any]) -> Any:
        """Handle weight conversion requests."""
        try:
            return convert_weight(args["value"], args["from_unit"], args["to_unit"])
        except ValueError as e:
            raise McpError(str(e))

    def handle_temperature_conversion(self, args: Dict[str, Any]) -> Any:
        """Handle temperature conversion requests."""
        try:
            return convert_temperature(args["value"], args["from_unit"], args["to_unit"])
        except ValueError as e:
            raise McpError(str(e))


def main():
    """Entry point for the MCP units server."""
    server = CookingUnitsServer(sys.stdin.buffer, sys.stdout.buffer, {})
    stdio_server(server)


if __name__ == "__main__":
    main()
