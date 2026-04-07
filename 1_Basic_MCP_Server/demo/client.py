## The FastMCP Client - https://gofastmcp.com/clients/client
## You provide a server source and the client automatically infers the appropriate transport mechanism.

from fastmcp import Client
import asyncio
from pathlib import Path

try:
    PARENT_DIR = Path(__file__).resolve().parent
except NameError:
    PARENT_DIR = Path.cwd()

async def main():
    # async with Client("http://localhost:8000/mcp") as client:     #Connects the client and server with streamable-http transport mechanism
    async with Client(PARENT_DIR / "server.py") as client:  #Connects the client and server with default stdio transport mechanism
        if client.is_connected():
            print("Connected to MCP Server")
            tools = await client.list_tools()
            for tool in tools:
                print(tool.name , '--', tool.description)

            # Call the add tool
            response = await client.call_tool("add", {"a": 1, "b": 5})
            print(response.structured_content['result'])
        else:
            print("Failed to connect to MCP Server")


if __name__ == "__main__":
    asyncio.run(main())


## Usage 
## Using uv to run the client
## uv run client.py

## Using python to run the client
## python client.py
