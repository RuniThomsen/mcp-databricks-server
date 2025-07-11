"""
Databricks MCP Server (Fixed Version)

This module provides MCP (Model Context Protocol) tools for interacting with Databricks.
It includes functionality for executing SQL queries and managing Databricks resources.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent
from databricks import sql


class DatabricksMCPServer:
    """MCP Server for Databricks integration."""
    
    def __init__(self):
        self.connection = None
        
    async def execute_sql(self, sql: str) -> Dict[str, Any]:
        """Execute SQL query against Databricks."""
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            
            # Fetch results
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            cursor.close()
            
            return {
                "success": True,
                "columns": columns,
                "rows": rows,
                "row_count": len(rows)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def list_tables(self, database: Optional[str] = None) -> Dict[str, Any]:
        """List tables in the specified database."""
        try:
            if database:
                sql = f"SHOW TABLES IN {database}"
            else:
                sql = "SHOW TABLES"
            return await self.execute_sql(sql)
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def describe_table(self, table_name: str) -> Dict[str, Any]:
        """Describe the schema of a table."""
        try:
            sql = f"DESCRIBE {table_name}"
            return await self.execute_sql(sql)
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _get_connection(self):
        """Get or create Databricks connection."""
        if self.connection is None:
            self.connection = sql.connect(
                server_hostname=os.getenv("DATABRICKS_HOST"),
                http_path=os.getenv("DATABRICKS_HTTP_PATH"),
                access_token=os.getenv("DATABRICKS_TOKEN")
            )
        return self.connection


async def main():
    """Main entry point."""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Validate required environment variables
    required_vars = ["DATABRICKS_HOST", "DATABRICKS_TOKEN", "DATABRICKS_HTTP_PATH"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        return
    
    # Create server instance
    databricks_server = DatabricksMCPServer()
    
    # Define tools
    async def handle_list_tools():
        """List available Databricks tools."""
        return [
            Tool(
                name="execute_sql",
                description="Execute a SQL query against Databricks",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "The SQL query to execute"
                        }
                    },
                    "required": ["sql"]
                }
            ),
            Tool(
                name="list_tables",
                description="List all tables in the current database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "database": {
                            "type": "string",
                            "description": "Database name (optional)"
                        }
                    }
                }
            ),
            Tool(
                name="describe_table",
                description="Get the schema of a specific table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to describe"
                        }
                    },
                    "required": ["table_name"]
                }
            )
        ]
    
    async def handle_call_tool(name: str, arguments: Dict[str, Any]):
        """Handle tool calls."""
        if name == "execute_sql":
            result = await databricks_server.execute_sql(arguments["sql"])
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        elif name == "list_tables":
            database = arguments.get("database")
            result = await databricks_server.list_tables(database)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        elif name == "describe_table":
            result = await databricks_server.describe_table(arguments["table_name"])
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await stdio_server().run(
            read_stream,
            write_stream,
            init_options={
                "server_name": "databricks-mcp",
                "server_version": "1.0.0",
            },
            list_tools=handle_list_tools,
            call_tool=handle_call_tool,
        )


if __name__ == "__main__":
    asyncio.run(main())
