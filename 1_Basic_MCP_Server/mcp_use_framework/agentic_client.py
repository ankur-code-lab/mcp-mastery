import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

try:
    PARENT_DIR = Path(__file__).resolve().parent
except NameError:
    PARENT_DIR = Path.cwd()

server_file = PARENT_DIR / "server.py"

async def main():

    ## Initialize the MCP Client with the server using stdio transport
    config = MCPClient({
        "mcpServers": {
            "weather": {
                "command": "python",
                "args": [str(server_file)]
            }
        }
    })

    ## Initialize the MCP Client with the server using streamable-http transport
    # config = MCPClient({
    #     "mcpServers": {
    #         "weather": {
    #             "url": "http://localhost:8000/mcp"
    #         }
    #     }
    # })




    # Initialize the LLM
    llm = ChatGroq(model="openai/gpt-oss-120b")


    # Intialize the MCP Agent
        
    agent = MCPAgent(
        llm=llm,
        client=config,
        max_steps=30
    )
    
    # Run the agent
    result = await agent.run("What is the weather like in New Delhi?")
    print(f"\nResult: {result}")

if __name__ == "__main__":
    asyncio.run(main())



