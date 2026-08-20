from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

async def mcp_client():
    client = MultiServerMCPClient({"moderation":
                                {"transport": "stdio",
                                    "command": "E:/my_projects/graph_agents/.venv/Scripts/python.exe",
                                    "args": ["E:/my_projects/graph_agents/server/moderation_mcp_server.py"]
                                    }})
    tools = await client.get_tools()
    print("Available MCP tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    return tools



asyncio.run(mcp_client())

