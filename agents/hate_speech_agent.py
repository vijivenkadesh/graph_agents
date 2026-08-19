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
    Analyze a message for hate speech using an LLM bound to word-count and
    profanity-check tools.

    Args:
        state: Agent state containing either 'hate_messages' (an ongoing
            conversation) or a fresh 'message' to analyze.

    Returns:
        A dict with key 'hate_messages' containing the updated message list
        on success, or 'error' with a description on failure. Callers should
        check for the 'error' key before proceeding.
    """

    try:
        llm_manager = LLMManager()
        llm = llm_manager.load_model()
        llm_with_tools = llm.bind_tools(tools=[word_count_tool,  profanity_check_tool])
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return {"error": "Failed to load model."}
    try:
        if not state['hate_messages']:
            prompt = HumanMessage(content=hate_speech_prompt_template.format(message=state['message']))
            messages = [system_prompt, prompt]

        else:
            messages = state["hate_messages"]
            
    except Exception as e:
        logging.error(f"Error preparing messages: {e}")
        return {"error": "Failed to prepare messages."}

    try:
        tool_response = llm_with_tools.invoke(input=messages)
    except Exception as e:
        logging.error(f"Error invoking LLM: {e}")
        return {"error": "Failed to invoke LLM."}
    
    return {"hate_messages": [tool_response]}


def hate_speech_agent(state: MessageState) -> Dict:
    """
    Analyze a message for hate speech using an LLM with structured output.

    Args:
        state: Agent state containing 'hate_messages' (an ongoing conversation).

    Returns:
        A dict with key 'hate_speech_agent_response' containing the analysis result.
    """
    try:
        messages = state["hate_messages"]
    except KeyError as e:
        logging.error(f"Missing 'hate_messages' in state: {e}")
        return {"error": "Missing 'hate_messages' in state."}

    try:
        llm_manager = LLMManager()
        llm = llm_manager.load_model()
        llm_with_structured_output = llm.with_structured_output(HateAgentResponse)
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return {"error": "Failed to load model."}

    try:
        response = llm_with_structured_output.invoke(messages)
    except Exception as e:
        logging.error(f"Error invoking LLM: {e}")
        return {"error": "Failed to invoke LLM."}

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