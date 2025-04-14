import os
from typing import Dict, List, Any, Optional
import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Database configuration
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# Model definitions
class ConnectDBParams(BaseModel):
    host: str
    user: str
    password: str
    database: str

class QueryParams(BaseModel):
    sql: str
    params: Optional[List[Any]] = None

class TableParams(BaseModel):
    table: str

# MCP Tool implementations
def connect_db(params: Dict[str, Any]) -> Dict[str, Any]:
    """Establish database connection"""
    try:
        conn = mysql.connector.connect(**params)
        return {"status": "success", "message": "Database connection established"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        raise HTTPException(status_code=500, detail=str(e))

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
        raise HTTPException(status_code=500, detail=str(e))

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
        raise HTTPException(status_code=500, detail=str(e))

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
        raise HTTPException(status_code=500, detail=str(e))

# MCP API endpoints
@app.post("/mcp/connect_db")
async def mcp_connect_db(params: ConnectDBParams):
    return connect_db(params.dict())

@app.post("/mcp/query")
async def mcp_query(params: QueryParams):
    return execute_query(params.dict())

@app.post("/mcp/execute")
async def mcp_execute(params: QueryParams):
    return execute_command(params.dict())

@app.get("/mcp/list_tables")
async def mcp_list_tables():
    return list_tables()

@app.post("/mcp/describe_table")
async def mcp_describe_table(params: TableParams):
    return describe_table(params.dict())

@app.get("/status")
async def get_status():
    """Get server status and available tools"""
    return {
        "status": "running",
        "tools": {
            "connect_db": "Establish database connection",
            "query": "Execute SELECT queries",
            "execute": "Execute INSERT, UPDATE, or DELETE queries",
            "list_tables": "List all tables",
            "describe_table": "Get table structure"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 