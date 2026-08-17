from sqlalchemy import create_engine, text
from model.message_state import MessageState
from urllib.parse import quote_plus
from core.config import get_settings

settings = get_settings()

passcode = settings.PASS_CODE

encoded_pass_code = quote_plus(string=passcode)

DATABASE_URL = (f"mysql+pymysql://root:{encoded_pass_code}@localhost:3306/moderation_db")

engine = create_engine(url=DATABASE_URL)


def save_moderation_result(state: MessageState) -> dict:
    decision = state["final_decision"]

    query = text("""
        INSERT INTO moderation_results
        (message, is_violation, category, confidence, reason)
        VALUES
        (:message, :is_violation, :category, :confidence, :reason)
    """)

    with engine.begin() as connection:
        connection.execute(
            query,
            {
                "message": state["message"],
                "is_violation": decision["is_violation"],
                "category": decision["category"],
                "confidence": decision["confidence"],
                "reason": decision["reason"],
            }
        )

    return {"status": "success"}


if __name__ == "__main__":
    test_state: MessageState = { "messages": "",
                           "message":"You are an Idiot",
                           "hate_speech_agent_response": {},
                           "profanity_agent_response": {},
                           "final_decision": {
                                           "message": "You are an Idiot",
                                           "is_violation": True,
                                           "category": "profanity",
                                           "confidence": 90,
                                           "reason": "Profanity word found",
                                       }}
    result = save_moderation_result(state=test_state)
    print(result)