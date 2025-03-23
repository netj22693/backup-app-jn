import streamlit as st

st.write("# BPMN diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")

st.write("-----")
st.write("#### Application process flow:")
st.image("Pictures/V2_pictures/BPMN overview.png")
st.write(" 5 stages of process - high level")


st.write("-----")
st.write("##### Data parsing process:")
st.image("Pictures/V2_pictures/BPMN data parsing.png")
st.write("Principle of data parsing process from XML")

st.write("-----")
st.write("##### Data validation process:")
st.image("Pictures/V2_pictures/BPMN validation.png")
st.write("""
- The application includes validation of the data <sum_total> (Invoice summary of price) against price per item <price>. 
- The same happens for <sum_total_services> against sum of <serice_price> in detail.""")
''
st.write("If match, application displays green success note.")
st.write("If not match, application displays warrning message and providing correct summary - calculated.")
''
st.write("In BOTH CASES application ALLOWS to continue to data vizualization step.")

st.write("-----")
st.write("##### Data vizualization process:")
st.image("Pictures/V2_pictures/BPMN data visualization2.png")
st.write("""
    Data visualization from the parsed data.
    - Overview of header and detail info including values which the app. calculated
    - Interactive table including pie chart and bar chart
    """  
    )