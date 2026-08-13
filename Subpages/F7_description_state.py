import streamlit as st 
from Subpages.Resources import Assets


st.write("# State flow")
''
''
st.write("""
- The **transport offer created in F7** is just first part of the business process.
- The term "offer" is used specifically as the next step is up to the customer to either accept or decline the offer. 
- Eventuelly, if no response till selected time (is set as part of offer generating process in F7), the offer gets expired and no more action will happen. 
- **If approved**, the transport can be organized and can start **accordingly to the preconfigured & calculated timeline in F7**.
- The full process is covered by relevant **states**.
""")

''
''
st.image("Pictures/Function_7/F7B_state_flow/F7_desc_state_business_process_BPMN_v1.svg")
st.caption("BPMN - Business process in context of the states.")


''
''
''
''
st.write("##### State flow diagram:")
''
st.write("""
- When offer created in F7 -> **Created**
- User needs to manually approve or reject via F7B UI -> **Approved**/**Rejected**
- If not approved till calculated time -> **Expired**
- If in **Approved** state, the rest of the workflow can happen:
    - **Transport preparation** - administration accordingly to Delivery service /SLA time
    - **Transport on the way** - physical move of the cargo accordingly to calculated time/distance
    - **Delivered**
""")

''
''
st.image(Assets.Images.f7_state_flow, width = 560)


''
''
''
''
st.write("##### State changes:")
''
st.write("""
- The **main method** is **Github Actions cron job** - runs **3x a day**
- In case that any milestone is in between last and next cron job run, **the application has also logic in the code to check states** for offers which should be displayed on the screen. 
- The combination of these 2 approaches helps to keep the data consistent with the calculated milestones when displayed on UI.
- The **states/milestones** are usually set within **few hours/days**.
""")

''
tab1, tab2 = st.tabs([
    "Cron job",
    "Application"
])

with tab1:
    ''
    st.image("Pictures/Function_7/F7B_state_flow/F7B_state_diagrams_UML_GHA_v1.svg", width=480)

with tab2:
    ''
    st.image("Pictures/Function_7/F7B_state_flow/F7B_state_diagrams_UML_app_v1.svg", width=480)


''
''
''
''
st.write("##### State BPMN process:")
''
st.write("- The Github Actions and the application logic described by BPMN")
''
st.image("Pictures/Function_7/F7B_state_flow/F7B_state_diagrams_BPMN_detail_v1.svg", width=500)

''
''
''
''
st.write("##### States from DB point of view:")
''
st.write("- Detail of how the states work from DB perspective")
''
st.image("Pictures/Function_7/F7B_state_flow/F7B_state_diagrams_ERD_v1.svg")

''
''
''
st.write("- Example of data based on states and methods changing them")
''
st.image("Pictures/Function_7/F7B_state_flow/F7B_state_diagrams_ERD_detail_v1.svg")





# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
	label = "Next page",
	page="Subpages/F7_description_dtd.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/east:"
	) 

st.page_link(
    label = "Previous page",
	page="Subpages/F7_description_ERD_DB.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/west:",
	) 