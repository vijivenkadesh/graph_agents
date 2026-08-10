from pydantic import BaseModel, Field
from typing import TypedDict



class AgentResponse(TypedDict):
    classification: str
    confidence: int