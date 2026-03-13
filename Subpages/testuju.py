import streamlit as st
from Subpages.F7_UI_image_generator import provide_ui_color_coding_image

transport = 'Truck'
transport = 'Train'
transport = 'Airplane'

dtd_a = 0
# dtd_a = 1

dtd_b = 0
# dtd_b = 1

truck_breaks = 0
# truck_breaks = 1




path = provide_ui_color_coding_image(transport, dtd_a, dtd_b, truck_breaks)

st.write(path)

st.image(path)