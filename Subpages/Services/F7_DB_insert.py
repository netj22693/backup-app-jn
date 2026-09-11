import streamlit as st
from app_db_connection import db_connection
from sqlalchemy import Column, Integer, String, Float, DateTime, Engine
from sqlalchemy.orm import declarative_base, Session
from Subpages.Dialog.F7_dialog import insert_db_not_complete,process_done


def insert_variables_offer(engine: Engine, data: dict):

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
    "currency" : data["currency"],
    "created_utc": data["created_utc"],
    "approve_till_utc": data["approve_till_utc"],
    "transport_start_utc": data["transport_start_utc"],
    "delivery_at_utc": data["delivery_at_utc"],
    "offer_state": data["offer_state"]
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
        created_utc = Column(DateTime(timezone=True))
        approve_till_utc = Column(DateTime(timezone=True))
        delivery_at_utc = Column(DateTime(timezone=True))
        offer_state = Column(String)
        transport_start_utc = Column(DateTime(timezone=True))
        
    with Session(engine) as session:
        new_offer = Offer(**mapped_data)
        session.add(new_offer)
        session.commit()

def insert_variables_delivery(engine: Engine, data: dict):

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

        offer_id = Column(String, primary_key=True)
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


def insert_variables_costs(engine: Engine, data: dict):

    mapped_data = {
    "offer_id": data["offer_id"],
    "currency": data["currency"],
    "distance_cost": data["distance_cost"],
    "dtd_from" : data["dtd_from"],
    "dtd_to" : data["dtd_to"],
    "shipment_value": data["shipment_value"],
    "insurance" : data["insurance"],
    "fragile" : data["fragile"],
    "danger" : data["danger"],
    }

    Base = declarative_base()

    class Costs(Base):
        __tablename__ = "costs"
        __table_args__ = {"schema": "function7"}

        offer_id = Column(String, primary_key=True)
        currency = Column(Integer)
        distance_cost = Column(Float)
        dtd_from = Column(Float)
        dtd_to = Column(Float)
        shipment_value = Column(Float)
        insurance = Column(Float)
        fragile = Column(Float)
        danger = Column(Float)


    with Session(engine) as session:
        new_offer = Costs(**mapped_data)
        session.add(new_offer)
        session.commit()


def insert_variables_extra_steps_time(engine: Engine, data: dict):

    mapped_data = {
    "offer_id": data["offer_id"],
    "truck_breaks": data["truck_breaks"],
    "shipment_transfer_dtd_from": data["shipment_transfer_dtd_from"],
    "shipment_transfer_dtd_to" : data["shipment_transfer_dtd_to"],
    "dtd_truck_if_not_truck_main" : data["dtd_truck_if_not_truck_main"],
    }

    Base = declarative_base()

    class Extra_steps_time(Base):
        __tablename__ = "extra_steps_time"
        __table_args__ = {"schema": "function7"}

        offer_id = Column(String, primary_key=True)
        truck_breaks = Column(Float)
        shipment_transfer_dtd_from = Column(Float)
        shipment_transfer_dtd_to = Column(Float)
        dtd_truck_if_not_truck_main = Column(Float)


    with Session(engine) as session:
        new_offer = Extra_steps_time(**mapped_data)
        session.add(new_offer)
        session.commit()

def insert_variables_go_green(engine: Engine, data: dict):

    mapped_data = {
        "offer_id": data["offer_id"],
        "main_route": data["main_route"],
        "from_dtd": data["from_dtd"],
        "to_dtd": data["to_dtd"],
        "transfer": data["transfer"],
        "total": data["total"]
    }

    Base = declarative_base()

    class Costs(Base):
        __tablename__ = "go_green"
        __table_args__ = {"schema": "function7"}

        offer_id = Column(String, primary_key=True)
        main_route = Column(Float)
        from_dtd = Column(Float)
        to_dtd = Column(Float)
        transfer = Column(Float)
        total = Column(Float)

    with Session(engine) as session:
        new_offer = Costs(**mapped_data)
        session.add(new_offer)
        session.commit()

def insert_variables_state_change_log(engine: Engine, data: dict):

    mapped_data = {
        "offer_id": data["offer_id"],
        "state_from": data["state_from"],
        "state_to": data["state_to"],
        "change_note": data["change_note"],
        "timestamp_utc": data["timestamp_utc"]
    }



    Base = declarative_base()

    class State_change_log(Base):
        __tablename__ = "state_change_log"
        __table_args__ = {"schema": "function7"}

        id = Column(Integer, primary_key=True)
        offer_id = Column(String)
        state_from = Column(String)
        state_to = Column(String)
        change_note = Column(String)
        timestamp_utc = Column(DateTime(timezone=True))

    with Session(engine) as session:
        new_offer = State_change_log(**mapped_data)
        session.add(new_offer)
        session.commit()


def insert_variables_offer_rating(engine: Engine, data: dict):
        
    mapped_data = {
        "offer_id": data["offer_id"],
        "rating_given": data["rating_given"],
        "delivery_at_utc": data["delivery_at_utc"],
        "rating_possible_till_utc": data["rating_possible_till_utc"]
    }


    Base = declarative_base()

    class State_change_log(Base):
        __tablename__ = "offer_rating"
        __table_args__ = {"schema": "function7"}

        id = Column(Integer, primary_key=True)
        offer_id = Column(String)
        rating_given = Column(Float)
        delivery_at_utc = Column(DateTime(timezone=True))
        rating_possible_till_utc = Column(DateTime(timezone=True))

    with Session(engine) as session:
        new_offer = State_change_log(**mapped_data)
        session.add(new_offer)
        session.commit()



# def save_to_db_main_stream(variables_extra_steps_time):
def save_to_db_main_stream(offer_number: dict, variables_offer: dict, variables_delivery: dict, variables_costs: dict, variables_extra_steps_time: dict, variables_go_green_dict: dict, state_change_log_dict: dict, offer_rating_dict: dict):

    db_engine = db_connection("F7")

    try:
        insert_variables_offer(db_engine, variables_offer)
        insert_variables_delivery(db_engine, variables_delivery)
        insert_variables_costs(db_engine, variables_costs)
        insert_variables_extra_steps_time(db_engine, variables_extra_steps_time)
        insert_variables_go_green(db_engine, variables_go_green_dict)
        insert_variables_state_change_log(db_engine, state_change_log_dict)
        insert_variables_offer_rating(db_engine, offer_rating_dict)

        process_done(offer_number)

    except Exception as e:
        print(f"DB insert failed: {e}")
        insert_db_not_complete()


# save_to_db_main_stream(variables_extra_steps_time_dict)




