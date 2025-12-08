import streamlit as st 

st.write("# DB & ERD:")

''
st.write("""
- The **data produced by F7 function** are inserted into **4 operational tables** - offer_id is the main connector
- The **F7 function does mapping** of the values before insert to follow the **logic of lookup tables**
- This DB design follows standards of Relational DB concept to be **scalable**
""")

''
''
st.image("Pictures/Function_7/F7_ERD_landscape_v2.svg")
''


sql_1 = """
-- JOIN Operational tables (a., b., c., e.)
SELECT *
FROM function7.offer a
  INNER JOIN function7.delivery b ON (a.offer_id = b.offer_id)
  INNER JOIN function7.costs c ON (a.offer_id = c.offer_id)
  INNER JOIN function7.extra_steps_time e ON (a.offer_id = e.offer_id);
"""

sql_2 = """
-- offer (a.) -> transport_type (f.)  & service (g.) -> sla (h.)
-- to get SLA time related to offers
SELECT
  a.offer_id,
  f.label AS transport_label,
  g.label AS service_label,
  h.time_sla
FROM function7.offer a
  INNER JOIN function7.sla h ON  (a.transport = h.transport_id_sla)
    -- 2nd key condition is a must - AND
    AND (a.service   = h.service_id_sla)
  INNER JOIN function7.transport_type f ON (a.transport = f.transport_id)
  INNER JOIN function7.service g ON (a.service = g.service_id);
"""

''
''
st.code(sql_1, language="sql")
st.code(sql_2, language="sql")





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
	page="Subpages/F7_description_variables.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/west:",
	) 