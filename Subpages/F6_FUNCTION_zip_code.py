import streamlit as st
import requests
import json
import pandas as pd
import sys


 


# ================= App Screen ============================

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

# ================== Rules for users ======================


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
    # st.image("Pictures/Function_6/F6_menu2_city.svg")
    st.write("- There can be **only 1 city per request**")
    # st.image("Pictures/Function_6/F6_menu2_city.svg")

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

# ================= API ============================

# FOR TESTINGS - to do not call API, if not neccessary

def TEST_get_request_2(city,country):

    json_data_api_2 ={
            "query": {
                "city": city,
                "state": "null",
                "country": country
            },
            "results": [
                "251 63",
                "110 00",
                "140 21",
                "140 78",
                "144 00",
            ]
        }
    
    return json_data_api_2


# For PROD purposes 
# https://app.zipcodebase.com/ - Bug: 1 api call is counted like 6
def get_api_2(city,country):

    api_key_1 = st.secrets["F6_api_1"]["password_1"]
    
    headers = { 
    "apikey": api_key_1}

    params = (
    ("city", city),
    ("country", country),
    );

    
    response = requests.get(f'https://app.zipcodebase.com/api/v1/code/city?apikey={api_key_1}', headers=headers, params=params, timeout=2);

    # st.write(f" write před return {response.text}")
    response = response.text
    # st.write(f" po response.text {response}")

    #Very important step to make for data type
    response = json.loads(response) 
    return response

        


# ================== User inputs ==========================

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
    
    ''
    ''
    if submit_button_1:
        
        # Firstly a validation that inputs provided -> if not, API will not be called
        if city == "":
                st.warning("Please provide City")
                
        else:
                
            try:
                # This is for PROD   /////////////////////////////////////////////// API 1
                f_data_json_2 = get_api_2(city,country)


                
                # This for TESTING
                # f_data_json_2 = TEST_get_request_2(city,country)
                # st.write(f" here data should be for parsing: {f_data_json_2}")
                
            except:
                st.warning("Apologies - The API is currently not available - connection timeout (2 seconds). Try again in 10-20 minutes.")
        
            # Data parsing from JSON
            ds = f_data_json_2['results']
            ds = list(map(str, ds))
            

            # logic for validation of income 
            b = len(ds)
            b = b - 1
            # st.write(b)
            

            if b == -1:
                st.warning("Your City is not related to the selected country or doesn't exist in DB")
                
            else:
                # data visualization APP
                data_serie = pd.Series(ds, name="ZIP codes",)
                data_serie.index += 1
                ''
                ''
                st.write(data_serie)
                

                # data translation into string with coma , for the (1) API
                string_for_api_1 = ",".join(ds)
                

                ''
                st.write("- Here **you can take the string** and put it into the box below (the second API/Search):")
                st.write(string_for_api_1)
                ''
                '' 
                st.write("- **(!) Important note:**")
                st.info("Because the API 2 (below) is a different application/works with different data -> it can happen that some of these ZIP codes might not be neccessary matching and the API 2 will NOT have the same data/ZIP codes")


                 

# ==========================================================================
# //////////////////////////////////////////////////////////////////////////
# ==========================================================================
# for testign purposes to do not call api 
def TEST_get_request(codes,country):

    data_json = {
	"query": {
		"codes": [
			codes
		],
		"country": country
	},
	"results": {
		"110007": [
			{
				"postal_code": "110 008888",
				"country_code": "CZ",
				"latitude": 50.3667,
				"longitude": 16.0417,
				"city": "Praha 1-Josefov",
				"state": "Hlavní město Praha",
				"city_en": "Praha 1-Josefov",
				"state_en": "Hlavní město Praha",
				"state_code": "52"
			},
			{
				"postal_code": "110 007777",
				"country_code": "CZ",
				"latitude": 50.3333,
				"longitude": 15.9167,
				"city": "Josefov",
				"state": "Hlavní město Praha",
				"city_en": "Josefov",
				"state_en": "Hlavní město Praha",
				"state_code": "52"
			}
		],
        "9999": [
			{
				"postal_code": "123",
				"country_code": "CZ",
				"latitude": 50.3667,
				"longitude": 16.0417,
				"city": "Praha 1-Josefov",
				"state": "Hlavní město Praha",
				"city_en": "Praha 1-Josefov",
				"state_en": "Hlavní město Praha",
				"state_code": "52"
			},
			{
				"postal_code": "456",
				"country_code": "CZ",
				"latitude": 50.3333,
				"longitude": 15.9167,
				"city": "Josefov",
				"state": "Hlavní město Praha",
				"city_en": "Josefov",
				"state_en": "Hlavní město Praha",
				"state_code": "52"
			}
		]
	}
}
  

    return data_json
 



# ============= Real API - GET request ===================== 

def  get_request(codes, country):

    # API ZIPCODESTACK
    api_url = "https://api.zipcodestack.com/v1/search"

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
    



# ================= App Scree ============================

''
''
''
st.write("#### (2) Validation of city based on ZIP code:")
''
''

# ================== Rules for users ======================


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
    
# ================== User inputs ==========================

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
    
    ''
    ''
    if st.form_submit_button(
        label="Submit",
        use_container_width=True,
        icon = ":material/apps:",
        ):

        
		# if/else logic for validation of input -> to do not call API  if no codes provided
		# Reason: if no ZIP code sprovided it will send 300+ ZIP codes (propably all under CZ or SK). BUT - 10 ZIP codes is charge as 1 API call -> this one single call would costs 30+ calls.
          
        if codes == "":
             st.warning("Please provide ZIP code(s)")
             st.stop()


        # 06-July-25: Bug fix/but also LIMITATION of this part of code 
        # Might not look that clean as there is multiple try-except and if conditions + nested while and for loops in them. Reason: this is only way I found how the streamlit is able to cover multiple happy/unhappy scenarios/states of the app and specifically for unhappy paths/scenarios completelly stop the script (specifically when get requests of api happens). I tried to split it under def() functions ended with exit() but the exit() function is not completelly stoping the streamlit and st.stop() is too big hard stop. 
        try: 
            # PROD /////////////////////////////////////////////// API 2
            f_data_json = get_request(codes, country)
            
            # For TEST purposes 
            #  f_data_json = TEST_get_request(codes, country)
            # st.write(f_data_json)

        except:
            st.warning("Apologies - The API is currently not available - connection timeout (2 seconds) stopped the request")
            st.stop()

        # ============ Data parsing from JSON ================
        #03-July-2025 - I am trying try/except for principle of not enought API requests 
        # {"message":"You used all your monthly requests. Please upgrade your plan at https://app.zipcodestack.com/subscription"}  -> try except block
            
        try:
            # ==== Parsing of the ZIP codes from JSON =======
            # Those are the same ZIP CODES as entered in user input
            # But in case that user will put a ZIP code which is not existing on the API side -> this mechanism will prevent from failing and just simply, will not get any response to show from the API. 
            # the JSON structure is built on dynamic value principle in segment
            # "results": { "11000": [{}],"12300": [{}]}   - the numbers (in string type) are the dynamic ones -> yes, those are the inputs from user -> JSON reflects that in the message
            
            # step 1 - the dynamic values to be parsed into list
            result_val = []
            
            # step 2 - number of items in the list 
            for result_jsn in f_data_json["results"]:
                result_jsn = str(result_jsn)
                result_val.append(result_jsn)
                
                #mapping into string
                result_val = list(map(str, result_val))
                #    st.write(f"after mapping into string: {result_val}")
                

            # step 2 - number of items in the list
            a = len(result_val)
            
            # step 3 - the number of items - 1 => we get number of indexes
            a = a - 1
            # st.write(a)
            

            if a == -1:
                st.warning("Your ZIP code(s) is not related to the selected country or doesn't exist in DB")
                
            else:
                # ---- inserted steps of visualization on the user screen ------
                # why here in the code? Because if the upper conditions passed visualization is needed, not earlier
                ''
                ''
                
                
                st.write("##### Results:")
                
                # split into tabs
                tab1,tab2 = st.tabs(["Table","Raw data"])

                # --------------------------------------------------------------
                
                # step 4 - setting a default index for for loop as O (to take the first dynamic number from the list as variable)
                index = 0
                
                # step 5 - while loop - to run until all the indexes checked/run
                while index <= a:
                        
                        # parsing of other values on the another JSON level
                        # the dynamic value are run based on the index number
                        result_val_single = result_val[index]
                        
                        #empty variables -> to be filled by data from the foor loop
                        postal_code_list = []
                        city_list = []
                        state_list = []
                        
                        for result in f_data_json["results"][result_val_single]:
                            tab2.write(f"- ZIP code: {result['postal_code']}")
                            tab2.write(f"- City name: {result['city_en']}")
                            tab2.write(f"- State: {result['state_en']}")
                            tab2.write(f"=====================================")
                            
                            postal_code_list.append(result['postal_code'])
                            city_list.append(result['city_en'])
                            state_list.append(result['state_en'])

                        # this increases the index number/move to the next item in the list
                        index = index + 1


                        # Note: important to keep this DF after the for loop -> to have the lists already filled with values (from the for loop)
                        result_dict = pd.DataFrame ({
                            "ZIP code" : postal_code_list,
                            "City name" : city_list,
                            "State" :  state_list                                
                        })
                        

                        # Tables - data visualization on the screen
                        
                        result_dict.index += 1	 
                                                
                        tab1.write(result_dict)                              
                            
                    
                    
        except:
            st.warning("Apologies, the limit of the API calls per month has been reached. It will be **renewed by 1st next month**. THIS PART OF APPLICATION IS CURRENTLY NOT AVAILABLE.")
            
