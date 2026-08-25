import streamlit as st
import pandas as pd
import plotly.express as px
from pandas.io.formats.style import Styler
from sqlalchemy import text
from typing import Optional, Dict, Tuple
from datetime import datetime, timezone
from sqlalchemy import Engine, Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base, Session

# ===== Data stying =====
def style_row(row: pd.Series, colors: pd.Series, column_name: str):
    rgb = colors.loc[row.name]

    return [
        f"color: rgb({rgb})" if column == column_name else ""
        for column in row.index
    ]


def get_columns_styled(df: pd.DataFrame, color_mapping: dict) -> Styler:

    def style_row(row):
        styles = []

        for column in row.index:
            color_column = color_mapping.get(column)

            if color_column:
                rgb = row[color_column]
                styles.append(f"color: rgb({rgb})")
            else:
                styles.append("")

        return styles

    return df.style.apply(style_row, axis=1)


def mapping_states(df: pd.DataFrame, mapping_dict: dict) -> pd.DataFrame:


    df.insert(1, "Icon", "")

    mapping = pd.DataFrame.from_dict(mapping_dict, orient="index")
  
    df["Icon"] = df["State"].map(mapping["symbol"])
    df["Color"] = df["State"].map(mapping["color"])

    # Note: 'State' mapping based on 'name' must be at the end as it changes to original lookup value 'APPROVE' -> 'Approved'
    df["State"] = df["State"].map(mapping["name"])

    return df



def get_styling_colors(df: pd.DataFrame) -> Styler:

    df[" "] = df.index + 1
    df = df.set_index(" ")

    # 1) This is separate variable for colors -> for styling because there will be drop from df before df_styled (styler has no .drop())
    colors = df["Color"]

    # 2) Drop from the origin DF
    df_display = df.drop(columns=["Color"])

    # Implementing colors + firmating - Note: must happen in 1 step here (if I split it both will not be applied)
    df_style = (
        df_display.style
        .apply(
            lambda row: style_row(row, colors, "Icon"), 
            axis=1
        )
        .format({
            "Final price": "{:,.2f}",
        })
    )

    return df_style


def df_styling_index_set_1(input_df: pd.DataFrame) -> pd.DataFrame:

    input_df[" "] = input_df.index + 1
    input_df = input_df.set_index(" ")

    return input_df


def df_change_column_name(input_df: pd.DataFrame) -> pd.DataFrame:
    
    dict_names = {
        "from_country" : "From country",
        "from_city" : "From city",
        "to_country" : "To country",
        "to_city" : "To city",
        "count" : "Count",
        "label" : "Label"
    }

    output_df = input_df.rename(columns=dict_names)

    return output_df

# ===== Mapping/parametrization =====
def get_parameters_countries(country_list: list) -> dict:
    
    params_list = []
    params_dict = {}

    for item in country_list:
        param = item.lower()
        params_list.append(param)
        params_dict[param] = item

    return params_dict

def create_parameters_for_sql(input: list, param_letter: str) -> Tuple[Dict[str, str], str]:
    '''
    Context: Parametrized queries using IN() in SQL are horribly slowing down returning result from PostgreSQL back to the code. Thus:

    THIS FUNCTION DOES DYNAMIC MAPPING to avoid SQL injection as the SQL query is built on f-string principle

    1) build of unique parameter e.g. t0, t1, t2 (depends on the param_letter)
    2) Creation of list [":t0", ":t1", ":t2"] -> list_params_keys[] filled with values
    3) Adding "key":"value" into dict params {} -> {"t0":"Airplane", "t1":"Train", "t2":"Truck"}
    4) Creation of string for sql ":t0, :t1, :t2" -> string_for_sql_in
    '''
    list_params_keys = []
    params = {}

    i = 0
    for value in input:
        param_name = param_letter + str(i)
        list_params_keys.append(":" + param_name)
        params[param_name] = value
        i = i + 1
    
    string_for_sql_in = ", ".join(list_params_keys)
    return params, string_for_sql_in

# ===== Charts =====
def create_pie_chart(df_input, x_data, y_data):
    
    chart = px.pie(
    df_input, 
    names = df_input[f"{x_data}"],
    values = df_input[f"{y_data}"]
    )

    # Adjustment to see 2 decimals always in the chart
    chart.update_traces(texttemplate="%{percent:.2%}")

    return chart



# ===== UI text adjustment =====
def singular_or_plural(input_value: float) -> str:
    '''
    Used for determining if day/days or hour/hours
    '''

    if input_value < 2:
        return ""
    
    else:
        return "s"


def display_state_and_symbol_mapped(input_state: str, mapping_dict: dict) -> str:

    state = mapping_dict.get(input_state)

    mapped_state = state["name"]
    rgb = state["color"]
    symbol = state["symbol"]
    
    st.markdown(
        f"Offer state: **{mapped_state}** <span style='color: rgb({rgb});'>{symbol}</span>",
        unsafe_allow_html=True
    )


def display_offer_logs(db_engine: Engine, sql_query: str, offer_id: str, mapping_dict: dict):

    df = pd.read_sql_query(sql=text(sql_query), con=db_engine, params={"offer_id" : offer_id}) 

    df.index = df.index + 1

    mapping = pd.DataFrame.from_dict(mapping_dict, orient="index")

    df["Sf"] = df["From"].map(mapping["symbol"])
    df["Sf_color"] = df["From"].map(mapping["color"])
    # Note: 'name' mapping based on 'name' must be at the end as it changes to original lookup value 'APPROVE' -> 'Approved'
    df["From"] = df["From"].map(mapping["name"])

    df["St"] = df["To"].map(mapping["symbol"])
    df["St_color"] = df["To"].map(mapping["color"])
    # Note: 'name' mapping based on 'name' must be at the end as it changes to original lookup value 'APPROVE' -> 'Approved'
    df["To"] = df["To"].map(mapping["name"])

    df = df[["From", "Sf", "Sf_color", "To", "St","St_color", "Info", "Timestamp UTC"]]

    # If None in these colums → create empty string ""
    df[["From", "Sf"]] = df[["From", "Sf"]].fillna("")

    df_style = get_columns_styled(
        df,
        { # Creation of simple dict for mapping
            "Sf": "Sf_color",
            "St": "St_color",
        }
    )

    # Display on UI 
    st.write("") # Woraround to make a space
    if df.empty:

        st.info(f"""
        - The offer {offer_id} has no log history available
        - This function was developed later on - starting by offer F7-322
        """)

    else:
        st.dataframe(
            df_style, 
            column_config={
                # None -> hides
                "Sf_color": None,
                "St_color": None,

                # Renaming columns
                "Sf": "",
                "St": ""
            }
        )

# ===== UI fallback =====
def data_empty_fallback_info(input_df: pd.DataFrame):

    '''
    UI fallback - for case when dataframes are empty (no data following search criteria)
    '''

    if input_df.empty:
        st.warning("No data in DB related to the selected date range")
        fallback = True

    else:
        fallback = False

    return fallback

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

# ===== Reset button ===== 
def reset_filters(list_countries_upper: list, tranport_types_list: list, currency_list: list):

    '''
    Reset button to clear all applied filters
    '''

    st.session_state["key_mlts_country_from"] = list_countries_upper
    st.session_state["key_mlts_country_to"] = list_countries_upper
    st.session_state["key_mlts_transport"] = tranport_types_list
    st.session_state["key_mlts_currency"] = currency_list
    st.session_state["key_checkbox_date"] = False
    st.session_state["key_sld_number_rows"] = 20