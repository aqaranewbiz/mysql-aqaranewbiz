import json
import sys
import os
from typing import Dict, Any

def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP requests"""
    try:
        if request["type"] == "getServerInfo":
            return {
                "type": "response",
                "id": request["id"],
                "result": {
                    "name": "Smithery MCP Server",
                    "version": "1.0.0",
                    "capabilities": ["mysql_query", "search"],
                    "mcp_server_type": "mysql" if os.getenv("MCP_SERVER_TYPE") == "mysql" else "perplexity"
                }
            }
        elif request["type"] == "executeTool":
            tool_name = request["tool"]
            params = request["params"]
            
            if tool_name == "mysql_query":
                # MySQL 쿼리 실행 로직
                return {
                    "type": "response",
                    "id": request["id"],
                    "result": {
                        "success": True,
                        "data": "MySQL query result"
                    }
                }
            elif tool_name == "search":
                # Perplexity 검색 로직
                return {
                    "type": "response",
                    "id": request["id"],
                    "result": {
                        "success": True,
                        "data": "Search result"
                    }
                }
            else:
                return {
                    "type": "error",
                    "id": request["id"],
                    "error": f"Unknown tool: {tool_name}"
                }
        else:
            return {
                "type": "error",
                "id": request["id"],
                "error": f"Unknown request type: {request['type']}"
            }
    except Exception as e:
        return {
            "type": "error",
            "id": request.get("id", "unknown"),
            "error": str(e)
        }

def main():
    """Main function to handle stdio communication"""
    while True:
        try:
            # Read request from stdin
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line)
            response = handle_request(request)
            
            # Write response to stdout
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            sys.stderr.write("Invalid JSON input\n")
            sys.stderr.flush()
        except Exception as e:
            sys.stderr.write(f"Error: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main() 