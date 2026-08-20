from pydantic import BaseModel, Field
from typing import TypedDict



class HateAgentResponse(TypedDict):
    is_hate_speech: bool
    category: str
    confidence: int
    reason: str


class ProfanityAgentResponse(TypedDict):
    is_profanity: bool
    category: str
    confidence: int
    reason: str



class FinalDecisionResponse(TypedDict):
    is_violation: bool
    category: str
    confidence: int
    reason: str
    cached: bool