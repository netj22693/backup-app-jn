import streamlit as st

st.write("### BPMN diagrams:")
st.write("*For better visibility - put cursor on the picture and click on the icon in the right upper corner")

st.write("-----")
st.write("#### Function 3 process flow:")
''
''
st.image("Pictures/Function_3/Function_3_BPMN process_3.png")
''
'''
Inputs to be entered by user and submited:
'''
''
st.image("Pictures/Function_3/delivery details.png", width = 200)
''
'''
Then application/function makes the calculation. In case of all inputs are okay, user can push download button for generating of invoice either in XML format or JSON. In case that user wants to change something in the original inputs, he can rewrite/change the inputs and then push Submit the button again...
'''
st.write("-----")
st.write("##### Application calculation process:")
''
''
st.image("Pictures/Function_3/Function_3_BPMN_calculation process.png")
''
'''
The calculation happens based on predefined inputs/costs which are part of application rules in the code. If the BPMN diagram would be transfared into the "application look" then it would be like this:
'''
''
st.image("Pictures/Function_3/Function_3_BPMN_calculation process_tables.png")
''
'''
The predefined values for calculations are:

 - Additional service/extra costs - Insurance - 15% from product price
 - Additional service/extra costs - Extended varanty - 10% from product price

 - And then specific costs for transport depending on Country, Transporting Company, Size of package
'''
''
st.image("Pictures/Function_3/Price_list.png")