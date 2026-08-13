from utils.llm_manager import LLMManager
from model.message_state import MessageState
from core.config import get_settings
from schema.agent_response import HateAgentResponse
from prompts.hate_speech_agent import system_prompt, hate_speech_prompt_template
from langchain.messages import HumanMessage
from tools.agent_tools import word_count_tool



def hate_speech_agent(state: MessageState) -> dict:
    llm_manager = LLMManager()
    llm = llm_manager.load_model()
    prompt = HumanMessage(content=hate_speech_prompt_template.format(message=state['message']))
    messages = [system_prompt, prompt]
    llm_with_tools = llm.bind_tools(tools=[word_count_tool])
    tool_response = llm_with_tools.invoke(input=messages)
    llm_with_structured_output = llm.with_structured_output(HateAgentResponse)

    # response = llm.invoke(input=message)
    response = llm_with_structured_output.invoke(messages)
    # result = response.content
    # state['hate_speech_agent_response'] = response
    # result = {'hate_speech_agent_response': response}
    return {'hate_speech_agent_response': response}



if __name__ == "__main__":
    input: MessageState = { "message":"That entire ethnic group is worthless.",
                           "hate_speech_agent_response": {},
                           "profanity_agent_response": {},
                           "final_decision": {}}
    result = hate_speech_agent(state=input)
    print(result)