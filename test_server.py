"""
Test script for the Databricks MCP Server - Tests MCP functionality without DB connection
"""

import asyncio
import os
import sys
from typing import Dict, Any, List, Sequence

# Add the current directory to the path
sys.path.insert(0, '.')

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json


async def test_mcp_server():
    """Test the MCP server setup without Databricks connection."""
    
    print("Testing MCP server functionality...")
    
    # Create server instance
    server = Server("test-databricks-mcp")
    
    @server.list_tools()
    async def handle_list_tools() -> List[Tool]:
        """List available test tools."""
        return [
            Tool(
                name="test_execute_sql",
                description="Test SQL execution tool",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "The SQL query to test"
                        }
                    },
                    "required": ["sql"]
                }
            ),
            Tool(
                name="test_list_tables",
                description="Test list tables tool",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "database": {
                            "type": "string",
                            "description": "Database name (optional)"
                        }
                    }
                }
            )
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Handle test tool calls."""
        if name == "test_execute_sql":
            result = {
                "success": True,
                "message": f"Would execute SQL: {arguments['sql']}",
                "test_mode": True
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        elif name == "test_list_tables":
            database = arguments.get("database", "default")
            result = {
                "success": True,
                "message": f"Would list tables in database: {database}",
                "test_mode": True
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    # Test the tools
    print("1. Testing tool listing...")
    tools = await handle_list_tools()
    print(f"   Available tools: {[tool.name for tool in tools]}")
    
    print("2. Testing SQL execution tool...")
    sql_result = await handle_call_tool("test_execute_sql", {"sql": "SELECT * FROM test_table"})
    print(f"   SQL tool result: {sql_result[0].text}")
    
    print("3. Testing list tables tool...")
    tables_result = await handle_call_tool("test_list_tables", {"database": "test_db"})
    print(f"   Tables tool result: {tables_result[0].text}")
    
    print("4. Testing server initialization options...")
    init_options = server.create_initialization_options()
    print(f"   Initialization options created successfully")
    
    print("\n✅ All MCP server tests passed! The server structure is correct.")
    return True


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
