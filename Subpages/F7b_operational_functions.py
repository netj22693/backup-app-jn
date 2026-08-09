import streamlit as st
import pandas as pd
from pandas.io.formats.style import Styler
from sqlalchemy import text
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Engine, Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base, Session

# ===== UI text adjustment =====
def singular_or_plural(input_value: float) -> str:
    '''
    Used for determining if day/days or hour/hours
    '''

    if input_value < 2:
        return ""
    
    else:
        return "s"


def display_offer_state(offer_state: str):

    st.write(f"""
    - Offer state: **{offer_state}**
    """)


def display_offer_logs(db_engine: Engine, sql_query: str, offer_id: str):

    df = pd.read_sql_query(sql=text(sql_query), con=db_engine, params={"offer_id" : offer_id}) 

    df.index = df.index + 1


    # Display on UI 
    ''
    st.write("""
    - Offer change logs (UTC time):
    """)

    if df.empty:
        st.info(f"""
        - The offer {offer_id} has no log history available
        - This function was developed later on - starting by offer F7-322
        """)

    else:
        st.write(df)



# ===== DB Update function =====
@st.dialog("Complete!")
def state_change_complete(offer_id: str, new_status: str):
    st.write(f"""
        - State change -> :green[**Complete**]
        - The offer **{offer_id}** has been changed to **{new_status}**
        """)

@st.dialog("Technical issue") 
def state_change_not_complete():
    st.write("""
        - State change **was not** complete -> :red[**Technical issue**]
        """)



def change_state_in_db(final_dialog: bool, engine: Engine, offer_id: str, was_state: str, new_state: str):

    # Preparation of data for insert
    change_note = {
        "APPROVED": "User changed via UI",
        "REJECTED": "User changed via UI",
        "EXPIRED": "System change",
        "TRANSPORT_PREPARATION": "System change",
        "TRANSPORT_ON_THE_WAY": "System change",
        "DELIVERED": "System change"
    }

    mapped_data_state_change_log = {
        "offer_id": offer_id,
        "state_from": was_state,
        "state_to": new_state,
        "change_note": change_note.get(new_state),
        "timestamp_utc": datetime.now(timezone.utc)
    }


    Base = declarative_base()


    # ORM class creation
    class Offer(Base):
        __tablename__ = "offer"
        __table_args__ = {"schema": "function7"}

        offer_id = Column(String, primary_key=True)
        offer_state = Column(String)


    class State_change_log(Base):
        __tablename__ = "state_change_log"
        __table_args__ = {"schema": "function7"}

        id = Column(Integer, primary_key=True)
        offer_id = Column(String)
        state_from = Column(String)
        state_to = Column(String)
        change_note = Column(String)
        timestamp_utc = Column(DateTime(timezone=True))


    try:

        # DB update
        with Session(engine) as session:

            # Update of OFFER table
            offer = session.get(Offer, offer_id)
            offer.offer_state = new_state

            # Create new record in STATE_CHANGE_LOG table
            state_change_log = State_change_log(**mapped_data_state_change_log)
            session.add(state_change_log)

            session.commit()

        # Final dialog
        if final_dialog == True:
            state_change_complete(offer_id, new_state)

    
    except Exception as e:
        print(f"DB Update fail: {e}")

        if final_dialog == True:
            state_change_not_complete()


# ===== State change function ===== 
def operational_update_of_states(df: pd.DataFrame, db_engine: Engine):

    utc_now = datetime.now(timezone.utc)

    updates = []

    for row in df.itertuples(index=False):

        #C1
        if (
            row.offer_state == "CREATED"
            and utc_now < row.approve_till_utc
            ):
            print(f"C1 - CREATED - State is okay - no action - offer: {row.offer_id}")

        elif (
            row.offer_state == "CREATED"
            and row.approve_till_utc < utc_now
            ):
            updates.append((row.offer_id, row.offer_state, "EXPIRED"))
            print(f"C1 - CREATED -> EXPIRED - offer: {row.offer_id}")

        # C2
        elif (
            row.offer_state == "APPROVED"
            and utc_now < row.approve_till_utc
            ):
            print(f"C2 - APPROVED - State is okay - no action - offer: {row.offer_id}")

        elif (
            row.offer_state == "APPROVED"
            and row.approve_till_utc < utc_now < row.transport_start_utc
            ):
            updates.append((row.offer_id, row.offer_state,"TRANSPORT_PREPARATION"))
            print(f"C2 - APPROVED -> TRANSPORT_PREPARATION - offer: {row.offer_id}")

        # C3
        elif (
            row.offer_state == "TRANSPORT_PREPARATION"
            and utc_now < row.transport_start_utc 
            ):
            print(f"C3 - TRANSPORT_PREPARATION - State is okay - no action - offer: {row.offer_id}")

        elif (
            row.offer_state == "TRANSPORT_PREPARATION"
            and row.transport_start_utc < utc_now < row.delivery_at_utc
            ):
            updates.append((row.offer_id, row.offer_state,"TRANSPORT_ON_THE_WAY"))
            print(f"C3 - TRANSPORT_PREPARATION -> TRANSPORT_ON_THE_WAY - offer: {row.offer_id}")

        # Fallback
        elif (
            row.offer_state == "APPROVED"
            and row.transport_start_utc < utc_now < row.delivery_at_utc
            ):
            updates.append((row.offer_id, row.offer_state,"TRANSPORT_ON_THE_WAY"))
            print(f"C3 - Fallback - APPROVED -> TRANSPORT_ON_THE_WAY - offer: {row.offer_id}")

        # C4
        elif (
            row.offer_state == "TRANSPORT_ON_THE_WAY"
            and utc_now < row.delivery_at_utc
            ):
            print(f"C4 - TRANSPORT_ON_THE_WAY - State is okay - no action - offer: {row.offer_id}")

        elif (
            row.offer_state == "TRANSPORT_ON_THE_WAY"
            and row.delivery_at_utc < utc_now
            ):
            updates.append((row.offer_id, row.offer_state, "DELIVERED"))
            print(f"C4 - TRANSPORT_ON_THE_WAY -> DELIVERED - offer: {row.offer_id}")


        # Fallback logic for case where there will longer period of scheduler run than distance time  
        elif (
            row.offer_state in ("APPROVED", "TRANSPORT_PREPARATION")
            and row.delivery_at_utc < utc_now
            ):
            updates.append((row.offer_id, row.offer_state, "DELIVERED"))
            print(f"Fallback - changed to DELIVERED - offer: {row.offer_id}")      

        # Falback to catch if any/condition is missed -> troubleshooting
        else:
            print(f"Undefined condition and state - offer: {row.offer_id}")


    for offer_id, was_state, new_state in updates:
        change_state_in_db(
            False,
            db_engine,
            offer_id,
            was_state,
            new_state
        )
        





# ===== Input validation ===== 
def input_validation(input: str) -> Optional[str]:
    '''  
    Simple logic to have correct format of 'offer_id' before query to DB

    Covers basic scenarios:
    1) user input is correct F7-number  - e.g. F7-123
    2) user input is "lazy" number format e.g. 123 -> adjustment F7-123
    3) user input is wrong generically - e.g. f123 -> return False

    '''
    if input.startswith("F7-"):
        return input

    if input.isdigit():
        input = "F7-" + input
        return input
    
    if input == "":
        st.warning("**Missing input** - Please provide **Offer number**")
        return None

    else:
        st.error(f"Invalid Offer format inserted - **{input}** is not valid. Valid format: F7-XXX")
        return None


# ===== Data stying =====
def mapping_states(df: pd.DataFrame, mapping_dict: dict) -> pd.DataFrame:


    df.insert(1, "Icon", "")

    mapping = pd.DataFrame.from_dict(mapping_dict, orient="index")
  
    df["Icon"] = df["State"].map(mapping["symbol"])
    df["Color"] = df["State"].map(mapping["color"])

    # Note: 'state' mapping based on 'name' must be at the end as it changes to original lookup value 'APPROVE' -> 'Approved'
    df["State"] = df["State"].map(mapping["name"])


    return df



def get_styling_colors(df: pd.DataFrame) -> Styler:

    df[" "] = df.index + 1
    df = df.set_index(" ")

    # 1) This is separate variable for colors -> for styling because there will be drop from df before df_styled (styler has no .drop())
    colors = df["Color"]

    # 2) Drop from the origin DF
    df_display = df.drop(columns=["Color"])

    def style_row(row):
        rgb = colors.loc[row.name]

        return [
            f"color: rgb({rgb})" if column == "Icon" else ""
            for column in row.index
        ]

    # Implementing colors + firmating - Note: must happen in 1 step here (if I split it both will not be applied)
    df_style = (
            df_display.style
            .apply(style_row, axis=1)
            .format({
                "Final price": "{:,.2f}",
            })
        )

    return df_style
