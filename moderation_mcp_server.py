from fastmcp import FastMCP
from tools.mcp_tools import word_count_tool, profanity_check_tool


mcp = FastMCP(name="moderation_mcp_server",
              )


mcp.add_tool(tool=word_count_tool)
mcp.add_tool(tool=profanity_check_tool)


if __name__ == "__main__":

    mcp.run(transport='stdio')