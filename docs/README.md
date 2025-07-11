# Databricks MCP Server

## Overview

This MCP server provides integration with Databricks, allowing you to execute SQL queries, manage tables, and interact with Databricks resources through the Model Context Protocol.

## Architecture

The server is built using the MCP (Model Context Protocol) framework and provides async/await support for all operations.

### Key Components

- **DatabricksMCPServer**: Main server class that handles MCP protocol communication
- **SQL Execution**: Direct SQL query execution against Databricks warehouses
- **Table Management**: Tools for listing and describing tables
- **Configuration**: Environment-based configuration for security

### Tools Provided

1. **execute_sql**: Execute arbitrary SQL queries
2. **list_tables**: List tables in databases
3. **describe_table**: Get table schema information

## Configuration

The server uses environment variables for configuration:

- `DATABRICKS_HOST`: Your Databricks workspace hostname
- `DATABRICKS_TOKEN`: Personal access token for authentication
- `DATABRICKS_HTTP_PATH`: SQL warehouse HTTP path

## Usage Examples

### Basic SQL Query

```python
await server.execute_sql("SELECT COUNT(*) FROM my_table")
```

### List Tables

```python
await server.list_tables("my_database")
```

### Describe Table

```python
await server.describe_table("my_database.my_table")
```

## Development

See the main README.md for development setup instructions.