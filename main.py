from utils.llm_manager import LLMManager
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from typing import List, Any
from tools.share_price import get_share_price

def main():
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    llm_with_tools = llm.bind_tools(tools=[get_share_price])
    messages: List[Any] = [HumanMessage(content="What is share price of Amzon")]
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    for tool_call in response.tool_calls:
        tool = tool_call.get("name")
        tool_result = get_share_price.invoke(tool_call["args"])
        messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]))

    # print(messages)

    result = llm_with_tools.invoke(input=messages)
    final_result = result.content
    print(final_result)


if __name__ == "__main__":
    main()
