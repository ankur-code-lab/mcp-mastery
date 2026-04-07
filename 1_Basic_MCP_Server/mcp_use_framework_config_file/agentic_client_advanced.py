import os
import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv

load_dotenv()

async def main():

    # Initialize the MCP Client with the server using stdio transport
    # config = MCPClient({
    #     "mcpServers": {
    #         "weather": {
    #             "command": "python",
    #             "args": ["/home/ankur-saxena/Documents/GenAI/MCP_/MCP-Mastery/1_Basic_MCP_Server/mcp_use_framework/server.py"]
    #         }
    #     }
    # })

    # Initialize the MCP Client with the server using streamable-http transport
    config = MCPClient(os.path.join(os.path.dirname(__file__), "mcp.json"))

    # Initialize the LLM
    llm = ChatGroq(model="openai/gpt-oss-120b")


    # Intialize the MCP Agent
        
    agent = MCPAgent(
        llm=llm,
        client=config,
        max_steps=30,
        use_server_manager=True # agent will automatically select the appropriate server based on the tool chosen by the LLM for each step. This avoids connecting to unnecessary servers and can improve performance with large numbers of available servers
    )
    
    # Run the agent
    # result = await agent.run("What is the weather like in New York?")
    
    query = input("Enter your query: ").strip().lower()
    if query in ["quit", "exit", "bye", "q"]:
        return False
    else:
        result = await agent.run(query)
        print(f"\nResult: {result}")

if __name__ == "__main__":
    while True:
        should_continue = asyncio.run(main())
        if should_continue is False:
            print("Exiting gracefully...")
            break



