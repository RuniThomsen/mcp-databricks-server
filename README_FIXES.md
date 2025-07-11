# MCP Databricks Server - Fixed Version

This repository contains a Model Context Protocol (MCP) server for interacting with Databricks.

## What Was Fixed

The original server had the following issues that have been resolved:

1. **MCP API Compatibility**: Updated to use the correct MCP 1.11.0 API
   - Replaced deprecated `stdio_transport()` with `stdio_server()`
   - Updated tool handling to use proper `handle_list_tools` and `handle_call_tool` functions
   - Fixed imports to use `mcp.server.stdio`

2. **Python Environment**: 
   - Configured proper Python virtual environment
   - Installed all required dependencies including the correct `mcp>=1.0.0` package
   - Updated MCP configuration to use the correct Python executable path

3. **Configuration**: 
   - Fixed path separators in configuration
   - Added missing DATABRICKS_TOKEN environment variable
   - Provided example environment configuration

## Setup Instructions

### 1. Install Dependencies

The required dependencies are already installed in the virtual environment:

```bash
# Dependencies installed:
# - mcp>=1.0.0
# - databricks-sql-connector>=3.0.0  
# - python-dotenv>=1.0.0
```

### 2. Configure Environment

Create a `.env` file in the mcp-databricks-server directory with your Databricks credentials:

```bash
cp .env.example .env
# Edit .env with your actual values
```

Required environment variables:
- `DATABRICKS_HOST`: Your Databricks workspace hostname
- `DATABRICKS_HTTP_PATH`: The HTTP path for your SQL warehouse
- `DATABRICKS_TOKEN`: Your Databricks access token

### 3. Update MCP Configuration

The MCP configuration in `.vscode/mcp.json` has been updated to use:
- Correct Python executable: `D:/repos/-KonicaMinolta/.venv/Scripts/python.exe`
- Fixed path to main.py: `d:/repos/mcp-databricks-server/main.py`
- Proper environment variables including DATABRICKS_TOKEN

### 4. Test the Server

Run the test script to verify MCP functionality:

```bash
D:/repos/-KonicaMinolta/.venv/Scripts/python.exe test_mcp.py
```

## Available Tools

The server provides the following MCP tools:

1. **execute_sql**: Execute a SQL query against Databricks
2. **list_tables**: List all tables in the current database
3. **describe_table**: Get the schema of a specific table

## Usage in VS Code

Once configured, the server will be available in VS Code through the MCP protocol. You can:

1. Execute SQL queries
2. List database tables
3. Describe table schemas
4. All through the VS Code Copilot interface

## Troubleshooting

### Common Issues:

1. **Python not found**: Make sure the MCP configuration uses the full path to the Python executable
2. **Missing dependencies**: All dependencies are installed in the virtual environment
3. **Connection errors**: Verify your Databricks credentials and network connectivity
4. **MCP API errors**: The server now uses the correct MCP 1.11.0 API

### Testing:

Run the test script to verify everything is working:
```bash
D:/repos/-KonicaMinolta/.venv/Scripts/python.exe test_mcp.py
```

This should output "MCP server test completed successfully!" if everything is configured correctly.
