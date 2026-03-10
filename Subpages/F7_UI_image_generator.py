import streamlit as st 

def provide_ui_image_path(transport, dtd_a, dtd_b, truck_breaks):

    a = "y" if dtd_a > 0 else "n"
    b = "y" if dtd_b > 0 else "n"
    c = "_with_break" if truck_breaks > 0 else ""

    path = f"Pictures/Function_7/F7_transport_flow_images/F7B_transport_flow_{transport}_dtd_A_{a}_dtd_B_{b}{c}.svg"

    return path