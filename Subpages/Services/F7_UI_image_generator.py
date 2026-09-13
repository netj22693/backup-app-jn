import streamlit as st 

def provide_ui_image_path(transport: str, dtd_a: int, dtd_b: int, truck_breaks: float) -> str:
    '''
    Based on variables/inputs generates path to the relevant image
    '''

    a = "y" if dtd_a > 0 else "n"
    b = "y" if dtd_b > 0 else "n"
    c = "_with_break" if truck_breaks > 0 else ""

    path = f"Pictures/Function_7/F7_transport_flow_images/F7B_transport_flow_{transport}_dtd_A_{a}_dtd_B_{b}{c}.svg"

    return path


def provide_ui_color_coding_image(transport: str, dtd_a: int, dtd_b: int, truck_breaks: float) -> str:
    '''
    Based on variables/inputs generates path to the relevant image
    '''

    a = "y" if dtd_a > 0 else "n"
    b = "y" if dtd_b > 0 else "n"

    if transport in ("Train", "Airplane"):

        # Distinguish if RED or YELLOW color or BOTH
        ta = "_transferYes" if dtd_a > 0 else "_transferNo"
        tb = "_transferYes" if dtd_b > 0 else "_transferNo"

        # Breaks not applicable for Train/Airplane
        breaks = ""

    elif transport == "Truck":
       
        # Transfer not applicable for Truck
        ta = ""
        tb = ""

        # with breaks 
        breaks = "_breaksYes" if truck_breaks > 0 else "_breaksNo"


    path = f"Pictures/Function_7/F7_transport_flow_images/F7B_color_coding_{transport}_dtd_A_{a}{ta}_dtd_B_{b}{tb}{breaks}.svg"
    
    return path