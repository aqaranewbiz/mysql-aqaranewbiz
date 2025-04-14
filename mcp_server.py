import json
import sys
import os
from typing import Dict, Any, Optional
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

def connect_db(params: Dict[str, Any]) -> Dict[str, Any]:
    """Establish database connection"""
    try:
        conn = mysql.connector.connect(**params)
        conn.close()
        return {"status": "success", "message": "Database connection established"}
    except Error as e:
        return {"status": "error", "message": str(e)}

def execute_query(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute SELECT query"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        if params.get('params'):
            cursor.execute(params['sql'], params['params'])
        else:
            cursor.execute(params['sql'])
            
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"status": "success", "results": results}
    except Error as e:
        return {"status": "error", "message": str(e)}

def execute_command(params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute INSERT, UPDATE, or DELETE query"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        if params.get('params'):
            cursor.execute(params['sql'], params['params'])
        else:
            cursor.execute(params['sql'])
            
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        
        return {
            "status": "success",
            "affected_rows": affected_rows
        }
    except Error as e:
        return {"status": "error", "message": str(e)}

def list_tables() -> Dict[str, Any]:
    """List all tables in database"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        conn.close()
        
        return {"status": "success", "tables": tables}
    except Error as e:
        return {"status": "error", "message": str(e)}

def describe_table(params: Dict[str, Any]) -> Dict[str, Any]:
    """Get table structure"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"DESCRIBE {params['table']}")
        structure = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"status": "success", "structure": structure}
    except Error as e:
        return {"status": "error", "message": str(e)}

def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP requests"""
    try:
        request_type = request.get("type")
        request_id = request.get("id")

        if request_type == "getServerInfo":
            return {
                "type": "response",
                "id": request_id,
                "result": {
                    "name": "@aqaranewbiz/mysql-aqaranewbiz",
                    "version": "1.0.0",
                    "tools": {
                        "connect_db": {
                            "description": "Establish connection to MySQL database using provided credentials"
                        },
                        "query": {
                            "description": "Execute SELECT queries with optional prepared statement parameters"
                        },
                        "execute": {
                            "description": "Execute INSERT, UPDATE, or DELETE queries with optional prepared statement parameters"
                        },
                        "list_tables": {
                            "description": "List all tables in the connected database"
                        },
                        "describe_table": {
                            "description": "Get table structure"
                        }
                    }
                }
            }
        elif request_type == "executeTool":
            tool_name = request.get("tool")
            params = request.get("params", {})
            
            if tool_name == "connect_db":
                result = connect_db(params)
            elif tool_name == "query":
                result = execute_query(params)
            elif tool_name == "execute":
                result = execute_command(params)
            elif tool_name == "list_tables":
                result = list_tables()
            elif tool_name == "describe_table":
                result = describe_table(params)
            else:
                return {
                    "type": "error",
                    "id": request_id,
                    "error": f"Unknown tool: {tool_name}"
                }
            
            if result.get("status") == "error":
                return {
                    "type": "error",
                    "id": request_id,
                    "error": result["message"]
                }
            
            return {
                "type": "response",
                "id": request_id,
                "result": result
            }
        else:
            return {
                "type": "error",
                "id": request_id,
                "error": f"Unknown request type: {request_type}"
            }
    except Exception as e:
        return {
            "type": "error",
            "id": request.get("id"),
            "error": str(e)
        }

def main():
    """Main function to handle stdin/stdout communication"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line)
            response = handle_request(request)
            
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        except json.JSONDecodeError as e:
            sys.stderr.write(f"Invalid JSON input: {str(e)}\n")
            sys.stderr.flush()
        except Exception as e:
            sys.stderr.write(f"Error: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main() 