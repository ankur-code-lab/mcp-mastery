from fastmcp import Client
from dotenv import load_dotenv
import os
import asyncio
from pathlib import Path
load_dotenv()

try:
    PARENT_DIR = Path(__file__).resolve().parent
except NameError:
    PARENT_DIR = Path.cwd()

async def main():
    async with Client("http://localhost:8000/mcp") as client:
        if client.is_connected():
            print("Connected to MCP Server")
            tools = await client.list_tools()
            for tool in tools:
                print(tool.name , '--', tool.description)

            # 📡 Call weather tools
            print("\n--- Getting Weather ---")
            response = await client.call_tool("get_realtime_weather", {"location": "mumbai", "api_key": os.getenv("WEATHERAPI_KEY"), "aqi": True, "lang": "en", "timeout_s": 10.0})
            print(response.structured_content)


if __name__ == "__main__":
    asyncio.run(main())

## Usage
## uv run client.py
## python client.py