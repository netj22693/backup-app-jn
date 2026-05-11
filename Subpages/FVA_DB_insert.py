import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float,DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime, timezone


def db_connection():

    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"

        engine = create_engine(conn_string)
        return engine

    except Exception as e:
        print(f"DB connection failed: {e}")



def insert_rating(data: dict):

    #engine creation
    engine = db_connection()

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
