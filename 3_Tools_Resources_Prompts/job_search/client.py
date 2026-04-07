import os
import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv
load_dotenv()

async def main():

    # Initialize the MCP Client with Server  
    config = MCPClient(os.path.join(os.path.dirname(__file__), "mcp.json"))
    
    # Initialize the LLM
    llm = ChatGroq(model="openai/gpt-oss-120b")

    #Initialize the MCP Agent
    agent = MCPAgent(llm=llm,
                    client=config,
                    max_steps=30,
                    use_server_manager=False)

    # Run the agent
    # result = await agent.run("Provide me Data Science jobs in Bangalore.")
    # ------------ Prompt Testing ------------
    # result = await agent.run("Analyze the job market for Data Scientist roles in Bangalore for top 2 results")
    # result = await agent.run("Give me some personalized job recommendations based on my resume.")
    # result = await agent.run("Create a match report for the jobs I have saved.")
    # Resource Testing
    # To list resources: "What MCP resources do you have access to?"
    # To read a specific resource: "Can you show me the content of the resume://default resource?"
    # To verify data integration: "List all the jobs I have saved using the jobs://saved resource."


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



