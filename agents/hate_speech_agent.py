from utils.llm_manager import LLMManager
from model.message_state import MessageState
from core.config import get_settings
from schema.agemt_response import AgentResponse



def sample_agent(state: MessageState) -> MessageState:
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    llm_with_structured_output = llm.with_structured_output(AgentResponse)
    message = state['message']
    # response = llm.invoke(input=message)
    response = llm_with_structured_output.invoke(input=message)
    # result = response.content
    state['hate_speech_agent_response'] = response
    return state