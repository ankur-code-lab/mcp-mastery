## https://pydantic.dev/docs/ai/mcp/client/


# agent_with_mcp.py
import asyncio

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP, MCPServerStdio
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

model = "groq:openai/gpt-oss-120b"

try:
    CURRENT_DIR = Path(__file__).resolve().parent
except:
    CURRENT_DIR = Path.cwd()

server_path = CURRENT_DIR / 'carbon_mcp_server.py'

## Connect to MCP server carbon_mcp_server.py running at http://localhost:8001/mcp and load all the tools that server exposes
server = MCPServerStreamableHTTP("http://localhost:8001/mcp")

## Connect to MCP Server carbon_mcp_server.py running in stdio mode
# server = MCPServerStdio('uv', args=['run', str(server_path)], timeout=10)

agent = Agent(
    model,
    toolsets=[server],
    system_prompt=(
        "You are an assistant that answers questions about "
        "UK electricity carbon intensity.\n"
        "- Use the MCP tools from the CarbonIntensityServer.\n"
        "- Never invent numbers; always call a tool when "
        "giving carbon intensity values.\n"
        "- For 'today' questions, prefer get_today_intensity_stats.\n"
        "- For 'right now' questions, prefer get_current_intensity."
    ),
)




'''
The MCP server automatically generates a list of instructions describing:

each tool, its arguments, what it returns.

This decorator: @agent.instructions, Adds those instructions to the LLM's system context

So the model knows what tools exist and how to call them. Without this, the LLM would not know that tools exist.
'''



@agent.instructions
async def mcp_server_instructions() -> str:
    """
    Add the MCP server's own instructions (including tool descriptions)
    into the agent's system context so the model knows what it can call.
    """
    return server.instructions


async def main() -> None:
    # Example question you mentioned
    # question = "What is the carbon intensity currently?"
    # question = "What is the carbon intensity before 2 days?"
    question = "What is the carbon intensity today?"
    result = await agent.run(question)

    print("User:", question)
    print("Assistant:", result.output)


if __name__ == "__main__":
    asyncio.run(main())
