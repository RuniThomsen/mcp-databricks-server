# MCP Databricks Server

MCP server for Databricks integration with validation tools and configuration.

## Features

- Execute SQL queries against Databricks
- List and describe tables
- Manage Databricks resources through MCP protocol
- Environment-based configuration
- Async/await support

## Installation

1. Clone this repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file with your Databricks credentials:

```env
# Your Databricks workspace URL (without https://)
DATABRICKS_HOST=your-workspace.azuredatabricks.net

# Your personal access token (generate from User Settings > Developer > Access Tokens)
DATABRICKS_TOKEN=your-access-token

# SQL warehouse HTTP path (found in SQL warehouse connection details)
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
```

## Usage

Run the MCP server:

```bash
python main.py
```

## Available Tools

- `execute_sql`: Execute SQL queries against Databricks
- `list_tables`: List all tables in the current or specified database
- `describe_table`: Get the schema of a specific table

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Format code:

```bash
black .
```

Type checking:

```bash
mypy .
```

## License

MIT License