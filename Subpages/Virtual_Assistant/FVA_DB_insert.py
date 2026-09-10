import logging
from app_logging import inicialization_logging
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime, timezone
from app_db_connection import db_connection

# Inicialization of logging
inicialization_logging()


def insert_rating_into_db(data: dict):

    #engine creation

    try:
        engine = db_connection(function_id="VA")

        mapped_data = {
        "uuid": data["uuid"],
        "thumb_rating": data["thumb"],
        "question": data["question"],
        "answer": data["answer"]
        }

        Base = declarative_base()

        class Rating(Base):
            __tablename__ = "rating"
            __table_args__ = {"schema": "virtual_assistant"}

            id = Column(Integer, primary_key=True, autoincrement=True)
            created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

            uuid = Column(String)
            thumb_rating = Column(Boolean)
            question = Column(String)
            answer = Column(String)

        with Session(engine) as session:
                new_offer = Rating(**mapped_data)
                session.add(new_offer)
                session.commit()

        logging.info(f"VA - DB insert complete")
        return True


    except Exception as e:
        logging.error(f"VA - DB insert failed: {e}")
        return False