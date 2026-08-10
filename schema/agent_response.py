from pydantic import BaseModel, Field
from typing import TypedDict



class AgentResponse(TypedDict):
    is_hate_speech: bool
    category: str
    confidence: int
    reson: str