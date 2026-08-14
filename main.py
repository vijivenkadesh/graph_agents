from utils.llm_manager import LLMManager
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from typing import List, Any, Annotated
from agents.hate_speech_agent import hate_speech_agent
from agents.profanity_agent import profanity_agent
from agents.manager_agent import manager_agent

from model.message_state import MessageState
# from prompts.hate_speech_agent import input
from graphs.agent_graph import graph
from core.config import get_settings
from dotenv import load_dotenv
load_dotenv()


def main():
    # llm_manager = LLMManager()
    # llm = llm_manager.load_model()
    # llm_with_tools = llm.bind_tools(tools=[get_share_price])
    # messages: List[Any] = [HumanMessage(content="What is share price of Amzon")]
    # response = llm_with_tools.invoke(messages)
    # messages.append(response)

    # for tool_call in response.tool_calls:
    #     tool = tool_call.get("name")
    #     tool_result = get_share_price.invoke(tool_call["args"])
    #     messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))

    # # print(messages)

    # result = llm_with_tools.invoke(input=messages)
    # final_result = result.content
    # print(final_result)

    # result1 = hate_speech_agent(state=input)
    # result2 = profanity_agent(state=input)
    # result3 = manager_agent(state=result2)
    
    # print(result1)
    # print("*"*20)
    # print(result2)
    # print("*"*100)
    # print(result3)
    message = input("Please enter message to analyze: ")
    input_state: MessageState = { "messages": "",
                           "message":message,
                           "hate_speech_agent_response": {},
                           "profanity_agent_response": {},
                           "final_decision": {}}
    result = graph.invoke(input=input_state)
    print(result)


if __name__ == "__main__":
    main()
