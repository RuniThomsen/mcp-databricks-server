"""
Test Databricks connection with configured credentials
"""
import os
import sys
from databricks import sql
from dotenv import load_dotenv

def test_databricks_connection():
    """Test the Databricks connection."""
    try:
        print("Testing Databricks connection...")
        print(f"Host: {os.getenv('DATABRICKS_HOST')}")
        print(f"HTTP Path: {os.getenv('DATABRICKS_HTTP_PATH')}")
        print(f"Token configured: {'Yes' if os.getenv('DATABRICKS_TOKEN') else 'No'}")
        
        # Create connection
        connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOST"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
        
        print("✅ Connection established successfully!")
        
        # Test a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test_value")
        result = cursor.fetchone()
        cursor.close()
        
        print(f"✅ Test query result: {result}")
        
        # List available databases
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        cursor.close()
        
        print(f"✅ Available databases: {[db[0] for db in databases[:5]]}")  # Show first 5
        
        connection.close()
        print("✅ All tests passed! Databricks connection is working.")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Load environment if .env file exists
    if os.path.exists('.env'):
        load_dotenv()
    
    success = test_databricks_connection()
    sys.exit(0 if success else 1)
