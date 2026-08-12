from utils.llm_manager import LLMManager
from model.message_state import MessageState
from core.config import get_settings
from schema.agent_response import ProfanityAgentResponse
from prompts.profanity_prompts import system_prompt, profanity_prompt_template
from langchain.messages import HumanMessage



def profanity_agent(state: MessageState, message: str) -> MessageState:
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    llm_with_structured_output = llm.with_structured_output(ProfanityAgentResponse)
    prompt = HumanMessage(content=profanity_prompt_template.format(message=message))
    messages = [system_prompt, prompt]
    # response = llm.invoke(input=message)
    response = llm_with_structured_output.invoke(messages)
    # result = response.content
    state['profanity_agent_response'] = response
    return state


if __name__ == "__main__":
    input: MessageState = {"hate_speech_agent_response": {},
                           "profanity_agent_response": {},
                           "final_decison": {}}
    result = profanity_agent(state=input, message="That entire ethnic group is worthless.")
    print(result)