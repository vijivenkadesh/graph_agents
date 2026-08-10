from typing import Annotated, TypedDict, Dict, Any




class MessageState(TypedDict):
    message: str
    hate_speech_agent_response: Dict[str, Any]
    profanity_agent_response: Dict[str, Any]
