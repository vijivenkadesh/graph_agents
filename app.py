from fastapi import FastAPI
from dotenv import load_dotenv
from core.logging_config import setup_logging

load_dotenv()
setup_logging(level="DEBUG")


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Agent Graph API. Use the /agent endpoint to analyze messages for hate speech and profanity."}


@app.post(path="/agent")
def agent_endpoint(message: str):
    from graphs.agent_graph import graph
    from model.message_state import MessageState

    input_state: MessageState = {
        "hate_messages": [],
        "profanity_messages": [],
        "message": message,
        "hate_speech_agent_response": {},
        "profanity_agent_response": {},
        "final_decision": {}
    }
    final_result = graph.invoke(input=input_state)
    return final_result