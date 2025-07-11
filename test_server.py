"""
Tests for Databricks MCP Server
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from main import DatabricksMCPServer


class TestDatabricksMCPServer:
    """Test cases for DatabricksMCPServer."""
    
    @pytest.fixture
    def server(self):
        """Create a test server instance."""
        return DatabricksMCPServer()
    
    @pytest.mark.asyncio
    async def test_execute_sql_success(self, server):
        """Test successful SQL execution."""
        mock_cursor = Mock()
        mock_cursor.description = [("column1",), ("column2",)]
        mock_cursor.fetchall.return_value = [("value1", "value2")]
        
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        server.connection = mock_connection
        
        result = await server.execute_sql("SELECT * FROM test_table")
        
        assert result["success"] is True
        assert result["columns"] == ["column1", "column2"]
        assert result["rows"] == [("value1", "value2")]
        assert result["row_count"] == 1
    
    @pytest.mark.asyncio
    async def test_execute_sql_error(self, server):
        """Test SQL execution with error."""
        mock_cursor = Mock()
        mock_cursor.execute.side_effect = Exception("SQL Error")
        
        mock_connection = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        server.connection = mock_connection
        
        result = await server.execute_sql("INVALID SQL")
        
        assert result["success"] is False
        assert "SQL Error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_list_tables(self, server):
        """Test listing tables."""
        with patch.object(server, 'execute_sql') as mock_execute:
            mock_execute.return_value = {
                "success": True,
                "columns": ["tableName"],
                "rows": [("table1",), ("table2",)]
            }
            
            result = await server.list_tables()
            mock_execute.assert_called_once_with("SHOW TABLES")
    
    @pytest.mark.asyncio
    async def test_list_tables_with_database(self, server):
        """Test listing tables in specific database."""
        with patch.object(server, 'execute_sql') as mock_execute:
            mock_execute.return_value = {
                "success": True,
                "columns": ["tableName"],
                "rows": [("table1",)]
            }
            
            result = await server.list_tables("my_database")
            mock_execute.assert_called_once_with("SHOW TABLES IN my_database")
    
    @pytest.mark.asyncio
    async def test_describe_table(self, server):
        """Test describing a table."""
        with patch.object(server, 'execute_sql') as mock_execute:
            mock_execute.return_value = {
                "success": True,
                "columns": ["col_name", "data_type"],
                "rows": [("id", "bigint"), ("name", "string")]
            }
            
            result = await server.describe_table("test_table")
            mock_execute.assert_called_once_with("DESCRIBE test_table")


if __name__ == "__main__":
    pytest.main([__file__])