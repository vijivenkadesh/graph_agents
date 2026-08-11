from langgraph.graph import StateGraph, START, END
from model.message_state import MessageState
from agents.hate_speech_agent import hate_speech_agent
from agents.profanity_agent import profanity_agent
from agents.manager_agent import manager_agent
from IPython.display import Image, display


builder = StateGraph(MessageState)

# adding agent nodes

builder.add_node("hate_speech_agent", hate_speech_agent)
builder.add_node("profanity_agent", profanity_agent)
builder.add_node("manager_agent", manager_agent)

# adding Start to agent connection edges

builder.add_edge(start_key=START, end_key="hate_speech_agent")
builder.add_edge(start_key=START, end_key="profanity_agent")

builder.add_edge(start_key="hate_speech_agent", end_key="manager_agent")
builder.add_edge(start_key="profanity_agent", end_key="manager_agent")

builder.add_edge(start_key="manager_agent", end_key=END)

graph = builder.compile()


# Just to debugging purpose
if __name__ == "__main__":
    png_data = graph.get_graph().draw_mermaid_png()

    with open("agent_graph.png", "wb") as f:
        f.write(png_data)

    print("Graph saved to agent_graph.png")