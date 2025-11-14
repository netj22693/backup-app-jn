import streamlit as st
import requests
import json
import pandas as pd


# ================= API 1 main logic in split into defs =================

# For PROD purposes 
# https://app.zipcodebase.com/ - Bug: 1 api call is counted like 6
def get_api_1(city,country):

    try:
        api_key_1 = st.secrets["F6_api_1"]["password_1"]
        
        headers = { 
        "apikey": api_key_1}

        params = (
        ("city", city),
        ("country", country),
        );

        response = requests.get(f'https://app.zipcodebase.com/api/v1/code/city?apikey={api_key_1}', headers=headers, params=params, timeout=2);

        response = response.text
        #Very important step to make for data type
        response = json.loads(response) 
        return response
    
    except Exception as e:
        print(e)
        st.warning("The API 1 is currently not available - connection was not established") 
        response = False
        return response


def api_1_data_parsing(data_json):

    # There can be only 2 types of JSON sent from source system
    # 1) API response - regular response -> try will pass
    # 2) API response - JSON with message note that limit reached -> goes to except

    try:
        # Data parsing from JSON
        ds = data_json['results']
        ds = list(map(str, ds))
        
        # logic for validation of income: if len = 0 -> no record in the JSON - "results":[]
        b = len(ds)
        
        if b == 0:
            st.warning("Your City is not related to the selected country or doesn't exist in DB")
            return False

        else:
            return ds
    
    except Exception as e:
        print(e)
        st.warning("API 1 limit has been reached - It will be **renewed by 1st next month**")
        return False
    

def api_1_adjusting_data_for_visualization(parsed_data_api_1):

    data_serie = pd.Series(parsed_data_api_1, name="ZIP codes",)
    data_serie.index += 1

    string_ap1 = ",".join(data_serie)

    return data_serie, string_ap1


def api_1_result_visualization(result_data_serie,result_string):

    # Result visualization on screen
    ''
    st.write(result_data_serie)
    ''
    st.write("- Here **you can take the string** and put it into the box below (the second API/Search):")
    st.write(result_string)
    ''
    '' 
    st.write("- **(!) Important note:**")
    st.info("Because the API 2 (below) is a different application/works with different data -> it can happen that some of these ZIP codes might not be neccessary matching and the API 2 will NOT have the same data/ZIP codes")


def submit_run_api_1(city, country):

    if not city:
        st.warning("Missing input - Please provide City")
        return

    data_json_api_1 = get_api_1(city, country)
    if not data_json_api_1:
        print("API 1 returned no data")
        return

    parsed_data_api_1 = api_1_data_parsing(data_json_api_1)
    if not parsed_data_api_1:
        print("API 1 parsing failed")
        return
    

    data_serie, string_ap1 = api_1_adjusting_data_for_visualization(parsed_data_api_1)

    api_1_result_visualization(data_serie, string_ap1)

    return



# ================= SCREEN USER ============================

st.write("# ZIP Code search:")
''
''
st.write("""
- API based 
- The information comes from (1) https://app.zipcodebase.com and (2) https://app.zipcodestack.com/
- **Note:** Because it is about 2 differnt applications sending the data, it can happen that sometimes there will not be 100% match 
""")


''
''
''
st.write("#### (1) ZIP code(s) based on City:")

''
with st.expander("How to use this function",
    icon=":material/help:"
    ):

    st.write("""
    - This function helps to provide **ZIP code number for particular city**
    - It is for **shipping purposes**
    """
    )

    ''
    st.write("- Firstly - Select country from the list (either CZ or SK): ")
    st.image("Pictures/Function_6/F6_menu_skcz.svg")

    ''
    ''
    ''
    st.write("- Secondly - Fill in the name of city:  can and cannot use capital leter: Prague/prague")
    st.write("- There can be **only 1 city per request**")


with st.expander("Some examples of Cities you can use",
    icon=":material/help:"
    ):

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

with st.expander("Known limitation",
    icon=":material/sync_problem:"
    ):

    st.write("""
    - Sometimes this API **is not able to establish connection**
    - It is probably on the Zipcodebase.com side
    - So the API call timeout is set to 2 seconds (which is max 2 calls) and then I set an intteruption in the code
    - They actually gurantee 99.9% uptime but **I have a Free subscription** of the API so I will have **probably less** :)
    - In case that connectivity not established and this app will display an alert. You can try again in 10-20 minutes. 
    - Sometimes the API connectivity works perfectly but sometimes not. 
    """
    )

# ================== SCREEN User inputs API 1 FORM ==========================

''
''
''
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
    
    # API 1 logic trigger
    # The 'if' is nested -> to keep results in the form box
    if submit_button_1: submit_run_api_1(city, country)




# ================= API 2 - App Screen ============================

''
''
''
st.write("#### (2) Validation of city based on ZIP code:")
''
''

with st.expander("How to use this function",
    icon=":material/help:"
    ):

    st.write("""
    - This function is for **validation of ZIP codes** to which **city, state/region** it belongs
    - It is for **shipping purposes**
    """
    )

    ''
    st.write("- Firstly - Select country from the list (either CZ or SK): ")
    st.image("Pictures/Function_6/F6_menu_skcz.svg")

    ''
    ''
    ''
    st.write("- Secondly - Fill in the ZIP code you would like to check:")
    st.image("Pictures/Function_6/F6_menu_post_single.svg")
    ''
    st.write("- **(!) RECOMMENDED:** If you want to check more, fill it like this: ZIPcode,ZIPcode,ZIPcode... and use a comma , as a separator")
    st.write("- **(!) BUT** have **MAX 10** ZIP codes in 1 request")
    st.image("Pictures/Function_6/F6_menu_post_multiple.svg")
    ''
    st.caption("** This approach of multiple inputs in one request helps to save/limit the number of API calls (source application limits this)")


    ''
    ''
    st.write("Negative scenarios:")
    st.write("- In case that your ZIP code input (one) is **NOT** related to the CZ or SK country warning note will be displayed ")
    st.image("Pictures/Function_6/F6_menu_nozip.svg")
    st.write("- In case that your ZIP code is **NOT** related to the CZ or SK, but you provided multiple codes, then the exiting will be delivered the others not. E.g. 4 codes filled in (3 existing, 1 not) -> 3 will be delivered")

with st.expander("Some examples of ZIP codes you can use",
    icon=":material/help:"
    ):

    st.write("- In case that you do not have any/do not know, you can use any of these:")
    st.write("""
    - **CZ** - Czech Republic
        - 3 ZIP codes
        - 11000,25163,15800
    """
    )

    st.write("""
    - **SK** - Slovakia
        - 3 ZIP codes
        - 013 41,013 06,811 08 
    """
    )

with st.expander("Known limitation",
    icon=":material/sync_problem:"
    ):

    st.write("""
    - This API allows **only 300** calls/requests per month (Free subscription)
    """
    )
    

# ================= API 2 ============================

def  get_request(codes, country):

    try:
        # API ZIPCODESTACK
        api_url = st.secrets["F6_api_2"]["url"]
        api_key_2 = st.secrets["F6_api_2"]["password_2"]

        headers = { 
        "apikey": api_key_2}

        params = (
        ("codes",codes),
        ("country",country),
        );

        # get reguest
        api_1 = requests.get(api_url, headers=headers, params=params,  verify=False, timeout=2).text      
        f_data_json = json.loads(api_1)
        return f_data_json
    
    except Exception as e:
        print(e)
        st.warning("The API 2 is currently not available - connection was not established")
        return False


def parsing_api_2(input_data_json):

    # There can be only 2 types of JSON sent from source system
    # 1) API response - regular response -> try will pass
    # 2) API response - JSON with message note that limit reached -> goes to except

    try:
        result_val = []
        
        for result_jsn in input_data_json["results"]:
            result_jsn = str(result_jsn)
            result_val.append(result_jsn)
    
    except Exception as e:
        print(e) 
        st.warning("The API 2 limit has been reached - It will be **renewed by 1st next month**")
        return False

    result_val = list(map(str, result_val))

    num = len(result_val)    
    if num == 0:
        st.warning("Your ZIP code(s) is not related to the selected country or doesn't exist in DB")
        return False
    
    return result_val



def result_visualization(data_list, data_json):

    st.write("##### Results:")
            
    tab1,tab2 = st.tabs(["Table","Raw data"])

    for result_val_single in data_list:

        postal_code_list = []
        city_list = []
        state_list = []

        for result in data_json["results"][result_val_single]:
            tab2.write(f"- ZIP code: {result['postal_code']}")
            tab2.write(f"- City name: {result['city_en']}")
            tab2.write(f"- State: {result['state_en']}")
            tab2.write(f"=====================================")

            postal_code_list.append(result['postal_code'])
            city_list.append(result['city_en'])
            state_list.append(result['state_en'])

        # DF creation
        result_dict = pd.DataFrame({
            "ZIP code": postal_code_list,
            "City name": city_list,
            "State": state_list
        })

        result_dict.index += 1
        tab1.write(result_dict)      


def submit_run_api_2(codes_input, country_input):

    if not codes_input:
        st.warning("Missing input - ZIP code(s)")
        return

    data_json_api_2 = get_request(codes_input, country_input)
    if data_json_api_2 == False:
        return

    list_values_parsed = parsing_api_2(data_json_api_2)  
    if list_values_parsed == False:
        return

    result_visualization(list_values_parsed, data_json_api_2)



# ================== API 2 - USER SCREEN  ==========================

''
''
''
with st.form("Get city based on ZIP code(s)"):
    country = st.selectbox("Country:",
        ["CZ", "SK"],
        help="Select country you assume that your ZIP code is from. CZ - Czech Republic, SK - Slovakia",
        )
    
    codes = st.text_input("ZIP code",
        help = "You can put 1 or more ZIP codes. If more the format is: ZIPcode,ZIPcode,ZIPcode... To do not overwhelm the API, put MAX 10 ZIP codes in one search."
        )
    
    submit_button_api_2 = st.form_submit_button(
        label="Submit",
        use_container_width=True,
        icon = ":material/apps:",
        )

    if submit_button_api_2: submit_run_api_2(codes, country)




