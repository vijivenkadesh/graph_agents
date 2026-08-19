from utils.llm_manager import LLMManager
from model.message_state import MessageState
from core.config import get_settings
from schema.agent_response import ProfanityAgentResponse
from prompts.profanity_prompts import system_prompt, profanity_prompt_template
from langchain.messages import HumanMessage
from tools.agent_tools import word_count_tool, profanity_check_tool
import logging

logging.getLogger(__name__)


def profanity_agent_with_tools(state: MessageState) -> dict:

    try:
        llm_manager = LLMManager()
        llm = llm_manager.load_model()
        llm_with_tools = llm.bind_tools(tools=[word_count_tool, profanity_check_tool])

    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return {"error": "Failed to load model."}

    try:
        if not state['profanity_messages']:
            prompt = HumanMessage(content=profanity_prompt_template.format(message=state['message']))
            messages = [system_prompt, prompt]
            
        else:
            messages = state["profanity_messages"]
    except Exception as e:
        logging.error(f"Error preparing messages: {e}")
        return {"error": "Failed to prepare messages."}
    try:
        tool_response = llm_with_tools.invoke(input=messages)
    except Exception as e:
        logging.error(f"Error invoking LLM: {e}")
        return {"error": "Failed to invoke LLM."}
    
    return {"profanity_messages": [tool_response]}


def profanity_agent(state: MessageState) -> dict:
    try:
        llm_manager = LLMManager()
        llm = llm_manager.load_model()
        llm_with_structured_output = llm.with_structured_output(ProfanityAgentResponse)
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return {"error": "Failed to load model."}

    messages = state['profanity_messages']
    
    try:
        response = llm_with_structured_output.invoke(messages)
    except Exception as e:
        logging.error(f"Error invoking LLM: {e}")
        return {"error": "Failed to invoke LLM."}

    return {'profanity_agent_response': response}


if __name__ == "__main__":
    message = input("Please enter message to analyze: ")
    input_state: MessageState = { "hate_messages": [],
                                 "profanity_messages": [],
                           "message":message,
                           "hate_speech_agent_response": {},
                           "profanity_agent_response": {},
                           "final_decision": {}}
    final_result = profanity_agent(state=input_state)
    print(final_result)