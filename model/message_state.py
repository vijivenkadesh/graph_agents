from typing import Annotated, TypedDict, Dict, Any, Optional, List
from schema.agent_response import FinalDecisionResponse
import operator

def merge_dict(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    return {**a, **b}

class MessageState(TypedDict):
    # message: Annotated[str, operator.concat]
    hate_speech_agent_response: Annotated[Dict[str, Any], merge_dict]  
    profanity_agent_response: Annotated[Dict[str, Any], merge_dict]
    final_decison: Optional[FinalDecisionResponse]