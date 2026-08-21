from sqlalchemy import create_engine
from urllib.parse import quote_plus
from core.config import get_settings




class DatabaseManager:

    def get_engine(self):
        settings = get_settings()

        passcode = settings.PASS_CODE

        encoded_pass_code = quote_plus(string=passcode)

        # DATABASE_URL = (f"mysql+pymysql://root:{encoded_pass_code}@localhost:3306/moderation_db")
        DATABASE_URL = (f"postgresql+psycopg2://postgres:{encoded_pass_code}@localhost:5432/moderation_db")

        engine = create_engine(url=DATABASE_URL)

        return engine
