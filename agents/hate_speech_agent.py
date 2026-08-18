from utils.llm_manager import LLMManager
from model.message_state import MessageState
from schema.agent_response import HateAgentResponse
from prompts.hate_speech_agent import system_prompt, hate_speech_prompt_template
from langchain.messages import HumanMessage
from tools.agent_tools import word_count_tool,  profanity_check_tool
from typing import Dict
import logging

logging.getLogger(__name__)


def hate_speech_agent_with_tools(state: MessageState) -> Dict:
    """
    This is an agent with tools. Load the configured model and bind the tools and analize the message for hate speech.
    """
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    llm_with_tools = llm.bind_tools(tools=[word_count_tool,  profanity_check_tool])
    if not state['hate_messages']:
        prompt = HumanMessage(content=hate_speech_prompt_template.format(message=state['message']))
        messages = [system_prompt, prompt]

    else:
        messages = state["hate_messages"]
    
    tool_response = llm_with_tools.invoke(input=messages)
    # state['messages'] = tool_response
    # llm_with_structured_output = llm.with_structured_output(HateAgentResponse)

    # response = llm.invoke(input=message)
    # response = llm_with_structured_output.invoke(messages)
    # result = response.content
    # state['hate_speech_agent_response'] = response
    # result = {'hate_speech_agent_response': response}
    return {"hate_messages": [tool_response]}


def hate_speech_agent(state: MessageState) -> Dict:
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    messages = state["hate_messages"]
    # state['messages'] = tool_response
    llm_with_structured_output = llm.with_structured_output(HateAgentResponse)

    # response = llm.invoke(input=message)
    response = llm_with_structured_output.invoke(messages)
    # result = response.content
    # state['hate_speech_agent_response'] = response
    # result = {'hate_speech_agent_response': response}
    return {'hate_speech_agent_response': response}



if __name__ == "__main__":
    message = input("Please enter message to analyze: ")
    input_state: MessageState = { "hate_messages": [],
                                 "profanity_messages": [],
                           "message":message,
                           "hate_speech_agent_response": {},
                           "profanity_agent_response": {},
                           "final_decision": {}}
    result = hate_speech_agent(state=input_state)
    print(result)