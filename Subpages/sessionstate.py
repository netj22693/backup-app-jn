import streamlit as st
import xml.etree.ElementTree as ET
import time
import plotly.express as px
import pandas as pd
import math
import pandasql as ps
from lxml import etree

# try: 
data_pie_sql3_3 = pd.DataFrame({
        "Category": ["A","B"],
        "Costs" : [1.11,2.22]

    })


fig = px.pie(
                    data_pie_sql3_3, 
                    names = "Category",
                    values = "Costs",
                    title = "(2) ...including add. services:"
                    )


fig.update_traces(texttemplate="%{percent:.3%}")

st.write(fig)


fig_pie_sql3_1.update_traces(texttemplate="%{percent:.2%}")