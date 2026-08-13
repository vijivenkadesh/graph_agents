from utils.llm_manager import LLMManager
from model.message_state import MessageState
from core.config import get_settings
from schema.agent_response import ProfanityAgentResponse
from prompts.profanity_prompts import system_prompt, profanity_prompt_template
from langchain.messages import HumanMessage
from tools.agent_tools import word_count_tool


def profanity_agent(state: MessageState) -> dict:
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    prompt = HumanMessage(content=profanity_prompt_template.format(message=state['message']))
    messages = [system_prompt, prompt]
    llm_with_tools = llm.bind_tools(tools=[word_count_tool])
    tool_response = llm_with_tools.invoke(input=messages)
    # state['messages'] = tool_response
    llm_with_structured_output = llm.with_structured_output(ProfanityAgentResponse)
    # response = llm.invoke(input=message)
    response = llm_with_structured_output.invoke(messages)
    # result = response.content
    # state['profanity_agent_response'] = response
    # result = {'profanity_agent_response': response}
    return {'profanity_agent_response': response, "messages": tool_response}


if __name__ == "__main__":
    input: MessageState = { "messages": "",
                           "message":"That entire ethnic group is worthless.",
                           "hate_speech_agent_response": {},
                           "profanity_agent_response": {},
                           "final_decision": {}}
    result = profanity_agent(state=input)
    print(result)