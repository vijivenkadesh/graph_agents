import hashlib
import re
from typing import Optional
import logging
from sqlalchemy import text
from utils.db_connection import DatabaseManager

from sentence_transformers import SentenceTransformer

looger = logging.getLogger(__name__)

_model = SentenceTransformer(model_name_or_path="all-MiniLM-L6-v2")
SIMILARITY_THRESHOLD: float = 0.90

def _normalize_messsage(message: str) -> str:

    return re.sub(pattern=r"", repl=" ", string=message.strip().lower())


def _hash_message(message: str) -> str:
    looger.info(msg=f"Processing the message: {message}")

    return hashlib.sha256(_normalize_messsage(message=message).encode(encoding="utf-8")).hexdigest()


def get_exact_cached_result(message: str) -> Optional[dict]:
    looger.info(msg=f"Getting exact match for the message: {message}")
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

def get_embedding(message: str) -> list[float]:

    embeddings = _model.encode(message, normalize_embeddings=True).tolist()

    return embeddings


def get_similar_cached_result(message: str) -> Optional[dict] | None:
    looger.info(msg=f"Getting Similar match for the message: {message}")
    db_manager = DatabaseManager()
    engine = db_manager.get_engine()

    embeddings = get_embedding(message=message)

    query = text("""
        SELECT is_violation, category, confidence, reason,
               1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM moderation_results
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT 1
    """)

    with engine.begin() as connection:
        row = connection.execute(statement=query,
                                 parameters={"embedding": embeddings}).fetchone()

    looger.info(msg=f"Similarity result for the message: {message} is {row.similarity if row else 'No match found'}")
    print(f"Similarity result for the message: {message} is {row.similarity if row else 'No match found'}")
    

    if row is None or row.similarity < SIMILARITY_THRESHOLD:
        return None

    return {
        "is_violation": row.is_violation,
        "category": row.category,
        "confidence": row.confidence,
        "reason": row.reason,
        "similarity": row.similarity,
        "cached": True,
    }



def get_cached_result(message: str) -> dict:
    exact_cache_result = get_exact_cached_result(message=message)

    if exact_cache_result:
        return exact_cache_result

    similarity_cache_result = get_similar_cached_result(message=message)

    return similarity_cache_result



if __name__ == "__main__":
    test_message = "screw you, you bastard"
    result = get_similar_cached_result(message=test_message)
    print(result)