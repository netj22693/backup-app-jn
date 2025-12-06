import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, Session


# TEST 
# europe_date_part = "06-Dec-25"
# europe_time_part = "12:04"
# cet_cest_now= "CET"
# offer_id = "F7-101"
# customer_approve_date = "11-Dec-25"
# customer_approve_time = "12:05"
# agreed_till_str = "5 days"
# selected_transport = "Truck"
# urgency = "Standard"
# cet_cest_now = "CET"
# overall_time_truck = 38.42
# delivery_dt_formated = "Monday - 15-Dec-25 by 10:00"
# final_price = 27513.23
# selected_currency = "euro"



def db_connection():

    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.gwc.azure.neon.tech/neondb?sslmode=require"

        engine = create_engine(conn_string)
        st.success("DB connected - ahoj z insert.py")
        return engine

    except:
        st.warning("DB not connected")
        # tady přidám nějaký end dialog nebo něco

def insert_variables_offer(engine, data):

    # parsing
    st.write(data)

    mapped_data = {
    "offer_id": data["offer_id"],
    "created_date": data["europe_date_part"],
    "created_time": data["europe_time_part"],
    "need_approve_date" : data["customer_approve_date"],
    "need_approve_time" : data["customer_approve_time"],
    "need_approve_days": data["agreed_till_str"],
    "transport" : data["selected_transport"],
    "service" : data["service"],
    "time_zone" : data["time_zone"],
    "time_overall" : data["time_overall"],
    "expected_delivery" : data["expected_delivery"],
    "final_price" : data["final_price"],
    "currency" : data["currency"]
    }

    Base = declarative_base()

    class Offer(Base):
        __tablename__ = "offer"
        __table_args__ = {"schema": "function7"}

        record_id = Column(Integer, primary_key=True)
        offer_id = Column(String)
        created_date = Column(String)
        created_time = Column(String)
        need_approve_date = Column(String)
        need_approve_time = Column(String)
        need_approve_days = Column(String)
        transport = Column(Integer)
        service = Column(Integer)
        time_zone = Column(Integer)
        time_overall = Column(Float)
        expected_delivery = Column(String)
        final_price = Column(Float)
        currency = Column(Integer)

    with Session(engine) as session:
        new_offer = Offer(**mapped_data)
        session.add(new_offer)
        session.commit()




# TEST

# offer_number_generated = "F1-129"
# country_code_from = "AT"
# from_city = "Prahahaha"
# from_city_extra_doortdoor = 10
# country_code_to = "DE"
# to_city = "Berlin"
# to_city_extra_doortdoor = 20
# distance = 888.88
# time_journey = 12.12
# time_dtd = 14



# variables_delivery_dict = {
#     "offer_id" : offer_number_generated,
#     "from_country" : country_code_from,
#     "from_city" : from_city,
#     "from_dtd" : from_city_extra_doortdoor,
#     "to_country" : country_code_to,
#     "to_city" : to_city,
#     "to_dtd" : to_city_extra_doortdoor,
#     "distance_length" : distance,
#     "distance_time" : time_journey,
#     "dtd_time" : time_dtd
# }

def insert_variables_delivery(engine, data):

    mapped_data = {
    "offer_id": data["offer_id"],
    "from_country": data["from_country"],
    "from_city": data["from_city"],
    "from_dtd" : data["from_dtd"],
    "to_country" : data["to_country"],
    "to_city": data["to_city"],
    "to_dtd" : data["to_dtd"],
    "distance_length" : data["distance_length"],
    "distance_time" : data["distance_time"],
    "dtd_time" : data["dtd_time"],
    }

    Base = declarative_base()

    class Delivery(Base):
        __tablename__ = "delivery"
        __table_args__ = {"schema": "function7"}

        offer_id = Column(Integer, primary_key=True)
        from_country = Column(String)
        from_city = Column(String)
        from_dtd = Column(Integer)
        to_country = Column(String)
        to_city = Column(String)
        to_dtd = Column(Integer)
        distance_length = Column(Float)
        distance_time = Column(Float)
        dtd_time = Column(Float)


    with Session(engine) as session:
        new_offer = Delivery(**mapped_data)
        session.add(new_offer)
        session.commit()


# def save_to_db_main_stream(variables_delivery):
def save_to_db_main_stream(variables_offer, variables_delivery):


    # tady bych dělla PDF ještě
    db_engine = db_connection()

    # Query_offer 
    insert_variables_offer(db_engine, variables_offer)
    insert_variables_delivery(db_engine, variables_delivery)



# save_to_db_main_stream(variables_delivery_dict)




@st.dialog("Go to:")
def db_py():


    ''
    st.page_link(
        label = "Function 3 - Description",
        page="Subpages/F3_F4_description.py",
        help="The button will redirect to the relevant page within this app.",
        width="stretch",
        icon=":material/code:",
        )

    st.page_link(
        label = "Function 3",
        page="Subpages/F3_FUNCTION_creation_of_XML.py",
        help="The button will redirect to the relevant page within this app.",
        width="stretch",
        icon=":material/play_circle:",
        )