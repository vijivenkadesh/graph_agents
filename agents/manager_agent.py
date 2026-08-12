from utils.llm_manager import LLMManager
from model.message_state import MessageState
from core.config import get_settings
from schema.agent_response import FinalDecisionResponse
from prompts.manager_agent_prompt import system_prompt, user_input_template


def manager_agent(state: MessageState, message: str) -> MessageState:
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    llm_with_structured_output = llm.with_structured_output(FinalDecisionResponse)
    user_prompt = user_input_template.format(message=message,
                               hate_speech_agent_response=state['hate_speech_agent_response'],
                               profanity_agent_response=state['profanity_agent_response'] )
    messages = [system_prompt, user_prompt]
    # message = state['message']
    # response = llm.invoke(input=message)
    response = llm_with_structured_output.invoke(messages)
    # result = response.content
    state['final_decison'] = response
    return state
