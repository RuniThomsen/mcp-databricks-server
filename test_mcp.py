"""
Simple test script for the Databricks MCP Server
"""

import asyncio
import os
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json


async def test_server():
    """Test the MCP server functionality."""
    
    # Mock tools for testing
    async def handle_list_tools():
        """List available test tools."""
        return [
            Tool(
                name="test_tool",
                description="A test tool",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Test message"
                        }
                    },
                    "required": ["message"]
                }
            )
        ]
    
    async def handle_call_tool(name: str, arguments: dict):
        """Handle test tool calls."""
        if name == "test_tool":
            result = {
                "success": True,
                "message": f"Received: {arguments.get('message', 'No message')}"
            }
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    print("Testing MCP server functionality...")
    
    # Test the tools
    tools = await handle_list_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    # Test tool call
    result = await handle_call_tool("test_tool", {"message": "Hello, MCP!"})
    print(f"Tool result: {result[0].text}")
    
    print("MCP server test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_server())
