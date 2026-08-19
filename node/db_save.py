from sqlalchemy import text
from model.message_state import MessageState

from utils.db_connection import DatabaseManager

def save_moderation_result(state: MessageState) -> dict:
    db_manager = DatabaseManager()
    engine = db_manager.get_engine()

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
    test_state: MessageState = { "hate_messages":[],
                                "profanity_messages":[],
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