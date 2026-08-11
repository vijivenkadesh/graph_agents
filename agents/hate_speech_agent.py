from utils.llm_manager import LLMManager
from model.message_state import MessageState
from core.config import get_settings
from schema.agent_response import HateAgentResponse
from prompts.hate_speech_agent import prompt



def hate_speech_agent(state: MessageState) -> MessageState:
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    llm_with_structured_output = llm.with_structured_output(HateAgentResponse)
    message = state['message']
    # response = llm.invoke(input=message)
    response = llm_with_structured_output.invoke(prompt)
    # result = response.content
    state['hate_speech_agent_response'] = response
    return state