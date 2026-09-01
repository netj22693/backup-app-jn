import pandas as pd
import streamlit as st
import logging
from datetime import datetime, timezone
from app_logging import inicialization_logging
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float,DateTime, Engine, update
from sqlalchemy.orm import declarative_base, Session



# ===== Inicialization for logging ===== 
inicialization_logging()

# ===== DB UI Dialogs ===== 
@st.dialog("Complete!")
def rating_complete(rating_result: float | int):
    st.write(f"""
    - Overall rating score: **{rating_result} / 5 ⭐**
    - Rating saved into DB -> :green[**Complete**]
    """)

@st.dialog("Technical issue") 
def rating_not_saved():
    st.write("""
    - Rating process not complete -> :red[**Technical issue**]
    """)

@st.dialog("Rating not saved")
def rating_already_submitted():
    st.write("""
    - Rating process **not** complete -> :blue[**Rating already given**]
    - There was a **concurrent user who gave the ratting** at the same time
    - **Search/reopen the offer again** to see the rating
    """)


# ===== DB save ===== 
def db_connection() -> Engine:

    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

        engine = create_engine(conn_string)
        logging.info("DB connection established")
        return engine

    except Exception as e:
        logging.error(f"DB connection failed: {e}")




def insert_rating_data_to_db(engine: Engine, data: dict, rating_result: int | float):

    Base = declarative_base()

    class OfferRating(Base):
        __tablename__ = "offer_rating"
        __table_args__ = {"schema": "function7"}

        id = Column(Integer, primary_key=True)
        offer_id = Column(String)
        rating_given = Column(Boolean)
        customer_service_value = Column(Integer)
        quality_service_value = Column(Integer)
        ontime_value = Column(Integer)
        condition_shipment_value = Column(Integer)
        recommendation_value = Column(Integer)
        recommendation_text = Column(String)
        overall_sum_value = Column(Integer)
        calculated_rating = Column(Float)
        user_text = Column(String)
        rating_given_utc = Column(DateTime(timezone=True))

    try:
        with Session(engine) as session:

            update_offer_rating_query = (
                update(OfferRating)
                .where(
                    OfferRating.offer_id == data["offer_id"],
                    OfferRating.rating_given == False
                )
                .values(
                    rating_given=True,
                    customer_service_value=data["customer_service_stars"]["value"],
                    quality_service_value=data["quality_stars"]["value"],
                    ontime_value=data["on_time_stars"]["value"],
                    condition_shipment_value=data["condition_shipment_stars"]["value"],
                    recommendation_value=data["recommendation"]["value"],
                    recommendation_text=data["recommendation"]["text_value"],
                    overall_sum_value=data["overall_rating"]["sum_value"],
                    calculated_rating=data["overall_rating"]["calculated_rating"],
                    user_text=data["user_text"],
                    rating_given_utc=data["rating_given_utc"],
                )
            )

            result = session.execute(update_offer_rating_query)


            if result.rowcount == 1:
                session.commit()

                logging.info("F7B Rating - DB save - complete")

                # rating_end_6
                rating_complete(rating_result)

            # This is to avoid overwritting due to CONCURRENCY
            # Rule: upper is WHERE statement OfferRating.rating_given == False
            # In case that there is 0 rows in DB (because if rating given it is changet to True) --> it menas that there was concurrent user who saved his rating earlier than this request of update
            else:
                session.rollback()

                logging.warning(
                    f"F7B Rating - Rating for offer_id={data['offer_id']} "
                    "was already submitted. CONCURRENCY."
                )

                # rating_end_7
                rating_already_submitted()


    except Exception as e:

        # Logging
        logging.error(f"F7B Rating - DB save - failed: {e}")

        # Technical issue with DB - final dialog
        rating_not_saved()


# ===== Rating calculation =====
def scale_recommendation(selected: str) -> int:

    scale = {
        "Yes": 5,
        "Maybe": 2.5,
        "No": 0
    }

    return scale.get(selected)

def mapping_user_text(text: str) -> str | None:

    return None if text == "" else text



def calculate_overall_rating(rating_dict: dict) -> dict:

    for key, item in rating_dict.items():

        number_stars = item["value"]

        coef = item["coefficient"]

        rating_dict[key] = {
        **item,  # whatever fields are before - '**' is placeholder for them
        "calculated_rating": round(number_stars * coef, 2),
        }

    # Sum of the values in the dict
    overall_rating_value = sum(
        item["value"]
        for item in rating_dict.values()
    )
        
    overall_rating_calculated = sum(
        item["calculated_rating"]
        for item in rating_dict.values()
    )

    # Extending of the dict
    rating_dict["overall_rating"] = {
        "sum_value": overall_rating_value,
        "calculated_rating" : overall_rating_calculated
    }

    return rating_dict


def adjust_rating_for_ui(value: dict) -> float | int:

    if value.is_integer():
        return int(value)

    return value


# ===== Orchestration of calculation =====
def calculate_rating_and_save_into_db(
    offer_id: str,
    customer_service_stars: int | None,
    quality_stars: int | None,
    on_time_stars: int | None,
    condition_shipment_stars: int | None,
    recommendation: str,
    user_text: str
    ): 
  
    rating_dict = {
        "customer_service_stars": {
            "value": customer_service_stars,
            "coefficient": 0.3
            },
        "quality_stars": {
            "value": quality_stars,
            "coefficient": 0.3              
        },
        "on_time_stars": {
            "value": on_time_stars,
            "coefficient": 0.1              
        },
        "condition_shipment_stars":{
            "value": condition_shipment_stars,
            "coefficient": 0.1              
        },
        "recommendation": {
            "value": scale_recommendation(recommendation),
            "text_value": recommendation,
            "coefficient": 0.2        
        }
    }


    rating_dict_extended = calculate_overall_rating(rating_dict)

    rating_dict_final = {"offer_id": offer_id, "rating_given_utc": datetime.now(timezone.utc)} | rating_dict_extended | {"user_text": mapping_user_text(user_text)}

    rating_result = adjust_rating_for_ui(rating_dict_final["overall_rating"]["calculated_rating"])

    db_engine = db_connection()

    insert_rating_data_to_db(db_engine, rating_dict_final, rating_result)



# ===== Core validation function =====
def make_rating_validation(df: pd.DataFrame) -> str:


    now = datetime.now(timezone.utc)

    if df.empty:
        return "END_RATING_NOT_POSSIBLE"

    else:
        row = df.iloc[0]

        if row["offer_state"] == "DELIVERED" and row["rating_given"] == True:
            return "END_RATING_DISPLAY"


        elif row["offer_state"] == "DELIVERED" and row["rating_given"] == False and row["rating_possible_till_utc"] < now:
            return "END_RATING_NOT_POSSIBLE_TIME_EXPIRED"

        elif row["offer_state"] == "DELIVERED" and row["rating_given"] == False and row["rating_possible_till_utc"] > now:
            return "END_RATING_CAN_BE_GIVEN"

        elif row["offer_state"] == "EXPIRED":
            return "END_RATING_NOT_POSSIBLE_STATE_EXPIRED"
        
        elif row["offer_state"] == "REJECTED":
            return "END_RATING_NOT_POSSIBLE_STATE_REJECTED"

        else:
            return "END_RATING_ONCE_DELIVERED"



# ===== UI functions -> vizualization =====
def display_rating_stars(count: int):

    return st.write(("★ " * count) + ("☆ " * (5 - count)))


def offer_rating_display_raiting(df:pd.DataFrame):

    row = df.iloc[0]

    with st.container(border=True):

        st.write(f"""##### Overall rating score: {adjust_rating_for_ui(row["calculated_rating"])} / 5 ⭐""")

        ''
        st.write("Customer service:")
        display_rating_stars(row["customer_service_value"])

        ''
        st.write("Overall quality of the delivery:")
        display_rating_stars(row["quality_service_value"])

        ''
        st.write("On-time delivery:")
        display_rating_stars(row["ontime_value"])

        ''
        st.write("Condition of the shipment:")
        display_rating_stars(row["condition_shipment_value"])

        ''
        st.write("Would you recommend our company:")
        st.write(f"""⦿ {row["recommendation_text"]}""")
        st.write("")

        # To display only if there is anything to display 
        if row["user_text"] is not None:

            st.write("Additional comment:")
            st.write(f""":gray[{row["user_text"]}]""")
            st.write("")

        else:
            pass


def normalize_rating(rating: int | None) -> int:

    '''
    Logic accordingly to the widgets (stars)
    0 stars -> None -> return 0
    1 star -> 0 -> return 1
    and so on
    '''


    return 0 if rating is None else rating + 1

def offer_rating_display_form(offer_id: str):

    with st.form(key="service_rating_form"):

        st.write("")
        st.success("Rate from **0** to **5** stars ⭐")

        st.write("")
        st.write("Customer service:")
        customer_service_stars: int | None = st.feedback(
            options="stars",
            key="customer_service"
        )

        st.write("")
        st.write("Overall quality of the delivery:")
        quality_stars: int | None = st.feedback(
            options="stars",
            key="quality_of_delivery"
        )

        st.write("")
        st.write("On-time delivery:")
        on_time_stars: int | None = st.feedback(
            options="stars",
            key="accuracy"
        )

        st.write("")
        st.write("Condition of the shipment:")
        condition_shipment_stars: int | None = st.feedback(
            options="stars",
            key="condition_shipment"
        )

        st.write("")
        st.write("Would you recommend our company:")
        recommendation: str = st.radio(
            "Would you recommend our company:",
            label_visibility="collapsed",
            options=["Yes","Maybe","No"],
            key="recomend_company"
        )


        st.write("")
        st.write("Anything you would like to share:")
        user_text: str = st.text_input(
            label="Free text",
            label_visibility="collapsed",
            max_chars=200,
            placeholder="Free text, not mandatory...",
            key="user_text"
        )


        st.write("")
        st.form_submit_button(
            label= "Submit",
            width="stretch",
            icon = ":material/apps:",
            on_click=lambda: calculate_rating_and_save_into_db(
                offer_id,
                normalize_rating(st.session_state.customer_service),
                normalize_rating(st.session_state.quality_of_delivery),
                normalize_rating(st.session_state.accuracy),
                normalize_rating(st.session_state.condition_shipment),
                st.session_state.recomend_company,
                st.session_state.user_text,
            )
        )


def display_offer_rating_ui_info(rating_end: str, df: pd.DataFrame):

    if rating_end == "END_RATING_DISPLAY":
        st.write(f"""Offer rating: **{adjust_rating_for_ui(df["calculated_rating"].iloc[0])} / 5** ⭐""")

    elif rating_end == "END_RATING_CAN_BE_GIVEN":
        st.write(f"""Offer rating: :green[**Form is available for rating → you can rate it now**]""")

    else:
        pass


def display_offer_rating_ui_tab(offer_id: str, rating_end: str, df: pd.DataFrame):


    if rating_end == "END_RATING_NOT_POSSIBLE":
        st.info("""
        - The rating feature **was not yet available** when this offer was processed. 
        - The feature was released on 27-Aug-2026
        """)

    elif rating_end == "END_RATING_ONCE_DELIVERED":
        st.info("Rating becomes available when the offer is marked as **Delivered**.")

    elif rating_end == "END_RATING_NOT_POSSIBLE_STATE_EXPIRED":
        st.info("Rating is unavailable for **Expired** offers.")

    elif rating_end == "END_RATING_NOT_POSSIBLE_STATE_REJECTED":
        st.info("Rating is unavailable for **Rejected** offers.")

    elif rating_end == "END_RATING_DISPLAY":
        offer_rating_display_raiting(df)

    elif rating_end == "END_RATING_NOT_POSSIBLE_TIME_EXPIRED":
        st.info("The rating period has **expired**. Ratings are available for **14 days** after delivery.")

    elif rating_end == "END_RATING_CAN_BE_GIVEN":  
        offer_rating_display_form(offer_id)