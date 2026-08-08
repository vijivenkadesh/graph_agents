from langchain_openai import ChatOpenAI
from core.config import get_settings


class LLMManager:

    def __init__(self, model: str = "") -> None:
        self.settings = get_settings()
        self.model = self.settings.MODEL


    def load_model(self):
        llm = ChatOpenAI(model=self.model, api_key=self.settings.OPENAI_API_KEY)
        return llm
