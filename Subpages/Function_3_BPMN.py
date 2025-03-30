import streamlit as st

st.write("# BPMN diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")

st.write("-----")
st.write("#### Function 3 process flow:")
''
''
st.image("Pictures/Function_3/Function_3_BPMN process_5.png")
''
'''
Inputs to be entered by user and submited:
'''
''
st.image("Pictures/Function_3/delivery details.png", width = 200)
''
'''
Then application/function makes the calculation. In case of all inputs are okay, user can push download button for generating of invoice either in XML format or JSON. In case that user wants to change something in the original inputs, he can rewrite/change the inputs and then push Submit button again...
'''
st.write("-----")
st.write("##### Application calculation process:")
''
''
st.image("Pictures/Function_3/Function_3_BPMN_calculation process_2.png")
''
'''
The calculation happens based on predefined inputs/costs which are part of application rules in the code. If the BPMN diagram would be transfared into the "application look" then it would be like this:
'''
''
st.image("Pictures/Function_3/Function_3_BPMN_calculation process_tables_2.png")
''
'''
The predefined values for calculations are:

 - Additional service/extra costs - Insurance - 15% from product price
 - Additional service/extra costs - Extended warranty - 10% from product price

 - And then specific costs for transport depending on Country, Transporting Company, Size of package
'''
''
st.image("Pictures/Function_3/Price_list.png")
''
''
st.write("-----")
st.write("#### Function 4 process flow:")
''
''
'''
In case that user wants to change file format of invoice generated in Function 3 step there is a possibility to use Function 4 for mapping into the other format than has been selected. Reason why to do this? The existing inovice file from Function 3 has uniquie ID and order number specific for the invoice and thus this conversion into the other file format will keep these unique IDs.
'''
''
''
st.image("Pictures/Function_4/Function_4_BPMN.png")