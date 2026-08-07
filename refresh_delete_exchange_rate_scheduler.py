import os
import pandas as pd
from sqlalchemy import create_engine, Engine, text
from datetime import datetime, timezone
from dotenv import load_dotenv
# import streamlit as st

# SQL query
sql_query_old_records = """
SELECT 
    id,
    created_at
                            
FROM function5.exchange_rate_data
                
WHERE created_at < NOW() AT TIME ZONE 'UTC' - INTERVAL '100 days'

ORDER BY created_at ASC
;"""

# Only for local testing - PROD uses Github Actions secrets
if os.path.exists(".env"):
    load_dotenv()

# For debbugging
print("RUN AT:", datetime.now(timezone.utc))

# DB connection
def get_db_connection() -> Engine:
    try: 

        password = os.getenv("NEON_DB_PASSWORD")
        endpoint = os.getenv("NEON_DB_ENDPOINT")

        # connection string
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

        engine = create_engine(conn_string)
        return engine
    
    except Exception as e:
        raise RuntimeError(f"DB connection failed: {e}")


def main():
    # Get engine
    db_engine = get_db_connection()

    # Pull data from DB
    df = pd.read_sql(sql_query_old_records, db_engine)

    # Logs -> visibility of deleted record ids
    print("----------")
    print(df)
    print("----------")
    print(f"Count of records to be deleted: {len(df)}")


    # Delete
    ids = df["id"].tolist()
    st.write(ids)

    try:
        with db_engine.begin() as conn:
            conn.execute(text("DELETE FROM function5.exchange_rate_data WHERE id = ANY(:ids)"), {"ids": ids})
            conn.execute(text("DELETE FROM function5.scheduler WHERE exchange_rate_id = ANY(:exchange_rate_id)"), {"exchange_rate_id": ids})
            conn.execute(text("DELETE FROM function5.api_kurzy_failure WHERE exchange_rate_id = ANY(:exchange_rate_id)"), {"exchange_rate_id": ids})
            conn.execute(text("DELETE FROM function5.api_freecurrency_failure WHERE exchange_rate_id = ANY(:exchange_rate_id)"), {"exchange_rate_id": ids})

        print("Delete successfully completed")

    except Exception as e:
        print(f"[Delete was not done]: {e}")
        raise
    
if __name__ == "__main__":
    main()

# ----- For test purposes ----- 
# if st.button("test"):
#     main()