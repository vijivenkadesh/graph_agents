from typing import Annotated, TypedDict, Dict, Any, List
from langgraph.graph.message import add_messages, AnyMessage

def merge_dict(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    return {**a, **b}

class MessageState(TypedDict):
    hate_messages: Annotated[List[AnyMessage], add_messages]
    profanity_messages: Annotated[List[AnyMessage], add_messages]
    message: str
    hate_speech_agent_response: Annotated[Dict[str, Any], merge_dict]  
    profanity_agent_response: Annotated[Dict[str, Any], merge_dict]
    final_decision: Annotated[Dict[str, Any], merge_dict]