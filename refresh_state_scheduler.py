import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String ,DateTime, Engine
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime, timezone
from dotenv import load_dotenv
# import streamlit as st



# ORM
Base = declarative_base()


class Offer(Base):
    __tablename__ = "offer"
    __table_args__ = {"schema": "function7"}

    offer_id = Column(String, primary_key=True)
    offer_state = Column(String)


class StateChangeLog(Base):
    __tablename__ = "state_change_log"
    __table_args__ = {"schema": "function7"}

    id = Column(Integer, primary_key=True)
    offer_id = Column(String)
    state_from = Column(String)
    state_to = Column(String)
    change_note = Column(String)
    timestamp_utc = Column(DateTime(timezone=True))


# SQL query 
sql_query_offer_status_validation_df = """
SELECT 
    a.offer_id,
    a.offer_state,
    a.created_utc,
    a.approve_till_utc,
    a.delivery_at_utc
                            
FROM function7.offer a
                
WHERE a.offer_state IN('CREATED', 'APPROVED', 'TRANSPORT_IN_PROGRESS')
    AND a.created_utc >= NOW() AT TIME ZONE 'UTC' - INTERVAL '20 days'

ORDER BY a.offer_id DESC

LIMIT 100
;"""

# Only for local testing - PROD uses Github Actions secrets
if os.path.exists(".env"):
    load_dotenv()

# For debbugging
print("RUN AT:", datetime.now(timezone.utc))

# DB connection
def get_db_connection():
    try: 

        password = os.getenv("NEON_DB_PASSWORD")
        endpoint = os.getenv("NEON_DB_ENDPOINT")

        # connection string
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

        engine = create_engine(conn_string)
        return engine
    
    except Exception as e:
        raise RuntimeError(f"DB connection failed: {e}")


def change_state_in_db(engine: Engine, offer_id: str, state_from: str, state_to: str):

    # GitHub Actions run id
    run_id = os.getenv("GITHUB_RUN_ID")
    # test
    # run_id = 111112

    mapped_data_state_change_log = {
        "offer_id": offer_id,
        "state_from": state_from,
        "state_to": state_to,
        "change_note": f"System change - GitHub Actions run: {run_id}",
        "timestamp_utc": datetime.now(timezone.utc)
    }


    # DB update
    with Session(engine) as session:

        # Update of OFFER table
        offer = session.get(Offer, offer_id)
        offer.offer_state = state_to

        # Create new record in STATE_CHANGE_LOG table
        state_change_log = StateChangeLog(**mapped_data_state_change_log)
        session.add(state_change_log)

        session.commit()




# ===== State change function ===== 
def operational_update_of_states(df: pd.DataFrame, db_engine: Engine):

    utc_now = datetime.now(timezone.utc)

    updates = []

    for row in df.itertuples(index=False):
        if (
            row.offer_state == "CREATED"
            and row.approve_till_utc < utc_now
            ):
            updates.append((row.offer_id, row.offer_state, "EXPIRED"))
            print(f"CREATED -> EXPIRED - offer: {row.offer_id}")

        elif (
            row.offer_state == "CREATED"
            and row.approve_till_utc > utc_now
            ):
            print(f"CREATED - State is okay - no action - offer: {row.offer_id}")

        elif (
            row.offer_state == "APPROVED"
            and row.approve_till_utc > utc_now
            ):
            print(f"APPROVED - State is okay - no action - offer: {row.offer_id}")

        elif (
            row.offer_state == "APPROVED"
            and row.approve_till_utc < utc_now
            ):
            updates.append((row.offer_id, row.offer_state,"TRANSPORT_IN_PROGRESS"))
            print(f"APPROVED -> TRANSPORT_IN_PROGRESS - offer: {row.offer_id}")

        elif (
            row.offer_state == "TRANSPORT_IN_PROGRESS"
            and row.delivery_at_utc < utc_now
            ):
            updates.append((row.offer_id, row.offer_state, "DELIVERED"))
            print(f"TRANSPORT_IN_PROGRESS -> DELIVERED - offer: {row.offer_id}")

        else:
            print(f"Undefined condition and state - offer: {row.offer_id}")


    for offer_id, was_state, new_state in updates:
        change_state_in_db(
            db_engine,
            offer_id,
            was_state,
            new_state
        )

def main():

    db_engine = get_db_connection()

    df_status_check = pd.read_sql(sql_query_offer_status_validation_df, db_engine)

    try:
        operational_update_of_states(df_status_check, db_engine)
        print("success")

    except Exception as e:
        print(f"[Main logic error]: {e}")
        raise
    
if __name__ == "__main__":
    main()

# ----- For test purposes ----- 
# if st.button("test"):
#     main()