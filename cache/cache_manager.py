import hashlib
import re
from typing import Optional
import logging
from sqlalchemy import text
from utils.db_connection import DatabaseManager

looger = logging.getLogger(__name__)

def _normalize_messsage(message: str) -> str:

    return re.sub(pattern=r"", repl=" ", string=message.strip().lower())


def _hash_message(message: str) -> str:
    looger.info(msg=f"Processing the message: {message}")

    return hashlib.sha256(_normalize_messsage(message=message).encode(encoding="utf-8")).hexdigest()


def get_cached_result(message: str) -> Optional[dict]:
    db_manager = DatabaseManager()
    engine = db_manager.get_engine()

    query = text("""
        SELECT is_violation, category, confidence, reason
        FROM moderation_results
        WHERE message_hash = :message_hash
        ORDER BY created_at DESC
        LIMIT 1
    """)

    with engine.begin() as connection:
        row = connection.execute(statement=query,
                                 parameters={"message_hash": _hash_message(message=message)}).fetchone()

    if not row:
        return None

    return {
        "is_violation": row.is_violation,
        "category": row.category,
        "confidence": row.confidence,
        "reason": row.reason,
        "cached": True,
    }

