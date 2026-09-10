import streamlit as st


def mapping_transport_type(input):

    mapping = {
        "Truck" : 1,
        "Train" : 2,
        "Airplane" : 3
    }

    return mapping.get(input)


def mapping_service(input):

    mapping = {
        "Slow" : 1,
        "Standard" : 2,
        "Express" : 3
    }

    return mapping.get(input)


def mapping_time_zone(input):

    mapping = {
        "CET" : 1,
        "CEST" : 2,
    }

    return mapping.get(input)


def mapping_currency(input):

    mapping = {
        "koruna" : 1,
        "euro" : 2,
    }

    return mapping.get(input)


def mapping_agreed_till(input):

    mapping = {
        "1 day" : 1,
        "2 days" : 2,
        "5 days" : 5,
        "7 days" : 7,
    }

    return mapping.get(input)