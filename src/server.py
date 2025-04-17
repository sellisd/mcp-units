#!/usr/bin/env python3

import sys
import json
from typing import Dict, Any

from converters.volume import convert_volume
from converters.weight import convert_weight
from converters.temperature import convert_temperature
from utils.validation import (
    validate_conversion_request,
    format_error_response,
    format_success_response,
    VOLUME_CONVERSION_SCHEMA,
    WEIGHT_CONVERSION_SCHEMA,
    TEMPERATURE_CONVERSION_SCHEMA,
)


class CookingUnitsServer:
    """MCP server for cooking unit conversions."""

    def __init__(self):
        self.tools = {
            "convert_volume": self.handle_volume_conversion,
            "convert_weight": self.handle_weight_conversion,
            "convert_temperature": self.handle_temperature_conversion,
        }

    def list_tools(self) -> Dict[str, Any]:
        """Return the list of available tools."""
        return {
            "tools": [
                {
                    "name": "convert_volume",
                    "description": "Convert between volume measurements (ml, l, cup, tbsp, tsp)",
                    "inputSchema": VOLUME_CONVERSION_SCHEMA,
                },
                {
                    "name": "convert_weight",
                    "description": "Convert between weight measurements (g, kg, oz, lb)",
                    "inputSchema": WEIGHT_CONVERSION_SCHEMA,
                },
                {
                    "name": "convert_temperature",
                    "description": "Convert between cooking temperature units (C, F)",
                    "inputSchema": TEMPERATURE_CONVERSION_SCHEMA,
                },
            ]
        }

    def handle_volume_conversion(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle volume conversion requests."""
        error = validate_conversion_request(args, VOLUME_CONVERSION_SCHEMA)
        if error:
            return format_error_response(error)

        try:
            result = convert_volume(args["value"], args["from_unit"], args["to_unit"])
            return format_success_response(result, args["to_unit"])
        except ValueError as e:
            return format_error_response(str(e))

    def handle_weight_conversion(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle weight conversion requests."""
        error = validate_conversion_request(args, WEIGHT_CONVERSION_SCHEMA)
        if error:
            return format_error_response(error)

        try:
            result = convert_weight(args["value"], args["from_unit"], args["to_unit"])
            return format_success_response(result, args["to_unit"])
        except ValueError as e:
            return format_error_response(str(e))

    def handle_temperature_conversion(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle temperature conversion requests."""
        error = validate_conversion_request(args, TEMPERATURE_CONVERSION_SCHEMA)
        if error:
            return format_error_response(error)

        try:
            result = convert_temperature(
                args["value"], args["from_unit"], args["to_unit"]
            )
            return format_success_response(result, args["to_unit"])
        except ValueError as e:
            return format_error_response(str(e))

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests."""
        method = request.get("method")

        if method == "listTools":
            return self.list_tools()

        if method == "callTool":
            tool_name = request.get("params", {}).get("name")
            tool_args = request.get("params", {}).get("arguments", {})

            if not tool_name:
                return format_error_response("Tool name is required")

            tool_handler = self.tools.get(tool_name)
            if not tool_handler:
                return format_error_response(f"Unknown tool: {tool_name}")

            return tool_handler(tool_args)

        return format_error_response(f"Unknown method: {method}")

    def run(self):
        """Run the MCP server, reading from stdin and writing to stdout."""
        while True:
            try:
                # Read request
                request_line = sys.stdin.readline()
                if not request_line:
                    break

                request = json.loads(request_line)

                # Process request
                response = self.handle_request(request)

                # Send response
                json.dump(response, sys.stdout)
                sys.stdout.write("\n")
                sys.stdout.flush()

            except json.JSONDecodeError:
                json.dump(format_error_response("Invalid JSON request"), sys.stdout)
                sys.stdout.write("\n")
                sys.stdout.flush()
            except Exception as e:
                json.dump(
                    format_error_response(f"Internal error: {str(e)}"), sys.stdout
                )
                sys.stdout.write("\n")
                sys.stdout.flush()


def main():
    """Entry point for the MCP units server."""
    server = CookingUnitsServer()
    server.run()


if __name__ == "__main__":
    main()
