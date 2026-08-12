from utils.llm_manager import LLMManager
from model.message_state import MessageState
from core.config import get_settings
from schema.agent_response import HateAgentResponse
from prompts.hate_speech_agent import system_prompt, hate_speech_prompt_template
from langchain.messages import HumanMessage



def hate_speech_agent(state: MessageState, message: str) -> MessageState:
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    llm_with_structured_output = llm.with_structured_output(HateAgentResponse)
    prompt = HumanMessage(content=hate_speech_prompt_template.format(message=message))
    messages = [system_prompt, prompt]
    # response = llm.invoke(input=message)
    response = llm_with_structured_output.invoke(messages)
    # result = response.content
    state['hate_speech_agent_response'] = response
    return state



if __name__ == "__main__":
    input: MessageState = {"hate_speech_agent_response": {},
                           "profanity_agent_response": {},
                           "final_decison": {}}
    result = hate_speech_agent(state=input, message="That entire ethnic group is worthless.")
    print(result)