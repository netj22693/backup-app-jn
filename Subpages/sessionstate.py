from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import streamlit as st

if st.button("cau"):
    prague_time = datetime.now(ZoneInfo("Europe/Prague"))

    offset_hours = int(prague_time.utcoffset().total_seconds() / 3600)

    st.write("prague", prague_time)
    st.write("offset", offset_hours)

    if offset_hours == 2:
        time_cet_cest = 'CEST'

    elif offset_hours == 1:
        time_cet_cest = 'CET'

    hours_result = 48


    gmt = time.gmtime()
    gmt_dt = datetime.fromtimestamp(time.mktime(gmt))

    st.write("gmt", gmt)
    st.write("gmt_dt", gmt_dt)

    delta = timedelta(hours = (hours_result + offset_hours))


    new_dt = gmt_dt + delta

    st.write(f"puvodni: {gmt_dt}")
    st.write(f"novy: {new_dt}")


    finale = new_dt.strftime("%A - %d-%b-%y by %H:%M")

    st.write(f"{finale} - {time_cet_cest}")

