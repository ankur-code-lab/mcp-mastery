from fastmcp import FastMCP

mcp = FastMCP('Demo MCP Server')


@mcp.tool()
def add(a: int, b: int) -> int:
    ''''Adds two numbers'''
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    '''Subtracts two numbers'''
    return a - b

if __name__ == '__main__':
    # mcp.run(transport="streamable-http")  #Runs the server with streamable-http transport mechanism
    mcp.run()                               #Runs the server with default stdio transport mechanism

## Usage
## uv run server.py
## python server.py
    