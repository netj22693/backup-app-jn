import streamlit as st
from Subpages.F6_operational_functions import orchestration_city_based_on_zipcode_search, orchestration_zipcode_based_on_city_search

# ================== UI  ==========================

st.write("# ZIP Code search:")
''
''
st.write("""
- API based 
- The data comes from 🟣 [Zipcodebase.com](https://app.zipcodebase.com) and 🟢 [Zipcodestack.com](https://app.zipcodestack.com/)
- **Note:** The function uses **two different external systems** sending the data -> sometimes there can be no match between them.
""")


# ================== UI FORM 1 ==========================
''
''
''
st.write("#### 🟣 Get ZIP code(s) based on City:")

''
with st.expander("How to use this form",
    icon=":material/help:"
    ):

    st.write("- Provides **ZIP code number(s) for particular city**")

    ''
    st.write("""
    - **Select country**
    - **Type name** of the city -> **(:red[!])** Only **one city** per request
    - Use **Submit button**
    """)

    ''
    st.write("- **Accepted formats:**")
    st.image("Pictures/Function_6/F6_rules_formatting_city_v1.svg")
    ''
    ''
    st.write("🟪 Few examples of cities you can use:")
    st.write("""
    - **CZ** - Czech Republic
        - Prague
        - Olomouc
        - Zlin
    """
    )

    st.write("""
    - **SK** - Slovakia
        - Kosice
        - Trencin
        - Banska Bystrica
    """
    )



with st.form("List of ZIP codes"):
    country = st.selectbox("Country:",
        ["CZ", "SK"],
        help="Select country, based on the City you are looking for. CZ - Czech Republic, SK - Slovakia",
        ).casefold()
    
    city = st.text_input("City",
        help="Only 1 city is allowed",
        ).capitalize()

    submit_button_1 = st.form_submit_button(
        label="Submit",
        use_container_width=True,
        icon = ":material/apps:",
        )
    
    # The 'if' is nested -> to keep results in the form box
    if submit_button_1: 
        orchestration_zipcode_based_on_city_search(city, country)




# ================== UI FORM 2 ==========================

''
''
''
st.write("#### 🟢 Get city based on ZIP code:")

''
with st.expander("How to use this form",
    icon=":material/help:"
    ):

    st.write("""- Provides **city, state/region** based on ZIP code(s)""")

    ''
    st.write("""
    - **Select country**
    - Type **ZIP code**
    - You can search for **multiple ZIP codes in one request** - limitation **10 ZIP codes**
    - If **multiple** ZIP codes, use **comma ,** as separator
    """)

    ''
    st.write("- **Accepted formats**:")
    st.image("Pictures/Function_6/F6_rules_formatting_v1.svg")

    ''
    ''
    ''
    ''
    st.write("🟩 Few examples of ZIP codes you can use:")

    st.write("""
    - **CZ** - Czech Republic
        - 110 00, 251 63, 158 00
    """
    )

    st.write("""
    - **SK** - Slovakia
        - 013 41, 013 06, 811 08 
    """
    )

with st.expander("API limitation",
    icon=":material/sync_problem:"
    ):

    st.write("""
    - This API allows **only 300** requests per month
    """
    )
    

# ================== API 2 - USER SCREEN  ==========================

''
with st.form("Get city based on ZIP code(s)"):
    country_code = st.selectbox("Country:",
        ["CZ", "SK"],
        help="Select country you assume that your ZIP code is from. CZ - Czech Republic, SK - Slovakia",
        )
    
    zipcode = st.text_input("ZIP code",
        help = "You can put 1 or more ZIP codes. If more the format is: ZIPcode,ZIPcode,ZIPcode... To do not overwhelm the API, put MAX 10 ZIP codes in one search."
        )
    
    submit_button_api_2 = st.form_submit_button(
        label="Submit",
        use_container_width=True,
        icon = ":material/apps:",
        )

    # The 'if' is nested -> to keep results in the form box
    if submit_button_api_2: 
        orchestration_city_based_on_zipcode_search(zipcode, country_code)