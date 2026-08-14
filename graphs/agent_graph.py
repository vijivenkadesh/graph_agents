from langgraph.graph import StateGraph, START, END
from model.message_state import MessageState
from agents.hate_speech_agent import hate_speech_agent
from agents.profanity_agent import profanity_agent, profanity_agent_with_tools
from agents.manager_agent import manager_agent
from IPython.display import Image, display
from langgraph.prebuilt import ToolNode, tools_condition
from tools.agent_tools import word_count_tool, profanity_check_tool


builder = StateGraph(MessageState)

# adding agent nodes

builder.add_node(node="hate_speech_agent", action=hate_speech_agent)
builder.add_node(node="profanity_agent", action=profanity_agent)
builder.add_node(node="profanity_agent_with_tools", action=profanity_agent_with_tools)
builder.add_node(node="manager_agent", action=manager_agent)
builder.add_node(node="hate_tools", action=ToolNode(tools=[word_count_tool]))
builder.add_node(node="profanity_tools", action=ToolNode(tools=[word_count_tool, profanity_check_tool]))

# adding Start to agent connection edges

builder.add_edge(start_key=START, end_key="hate_speech_agent")
builder.add_edge(start_key=START, end_key="profanity_agent_with_tools")
builder.add_conditional_edges(source="hate_speech_agent", path=tools_condition, path_map={"tools": "hate_tools", END: "manager_agent"})
builder.add_edge(start_key="hate_tools", end_key="hate_speech_agent")
builder.add_conditional_edges(source="profanity_agent_with_tools", path=tools_condition, path_map={"tools": "profanity_tools", END: "profanity_agent"})
builder.add_edge(start_key="profanity_tools", end_key="profanity_agent_with_tools")

# builder.add_edge(start_key="hate_speech_agent", end_key="manager_agent")
builder.add_edge(start_key="profanity_agent", end_key="manager_agent")

builder.add_edge(start_key="manager_agent", end_key=END)

graph = builder.compile()


# Just to debugging purpose
if __name__ == "__main__":
    png_data = graph.get_graph().draw_mermaid_png()

    with open("agent_graph.png", "wb") as f:
        f.write(png_data)

    print("Graph saved to agent_graph.png")