# MCP Cooking Units Converter

[![smithery badge](https://smithery.ai/badge/@sellisd/mcp-units)](https://smithery.ai/server/@sellisd/mcp-units)

mcp-name: io.github.username/mcp-units

**MCP Cooking Units Converter** is a Python package and MCP server for converting cooking measurements (volume, weight, temperature) between common units. It is designed for integration with MCP-compatible tools and VSCode extensions.

## Installation

### Installing via Smithery

To install Cooking Units Converter for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@sellisd/mcp-units):

```bash
npx -y @smithery/cli install @sellisd/mcp-units --client claude
```

### Manual Installation
1. Clone the repository:
```bash
git clone git@github.com:sellisd/mcp-units.git
cd mcp-units
```

2. Install:
```bash
uv pip install .  # For normal use
# OR
uv pip install -e .  # For development
```

## Usage

### Available Tools

The server provides the following conversion tools:

1. **Volume Conversion**
   - Convert between: ml, l, cup, tbsp, tsp
   - Example: 240ml → 1 cup

2. **Weight Conversion**
   - Convert between: g, kg, oz, lb
   - Example: 454g → 1 lb

3. **Temperature Conversion**
   - Convert between: Celsius (C), Fahrenheit (F)
   - Example: 180°C → 356°F

### Running the Server

```bash
uvx --with . python -m mcp_units.server
```

## Using with VSCode Extensions

This MCP server can be integrated with VSCode extensions that support the Model Context Protocol. Here's how to set it up:

1. Install an MCP-compatible VSCode extension (e.g., Roo)

2. Configure the extension to use this server in `.roo/mcp.json`:
   ```json
   {
     "mcpServers": {
       "units": {
         "command": "uvx",
         "args": [
           "--with",
           ".",
           "python",
           "-m",
           "mcp_units.server"
         ],
         "disabled": false
       }
     }
   }
   ```

## Contact

For questions, issues, or contributions, please visit the [GitHub repository](https://github.com/sellisd/mcp-units).

## License

This project is licensed under the MIT License.
