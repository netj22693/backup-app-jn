import streamlit as st
import requests
import json

# for testign purposes to do not call api 
def TEST_get_request(codes,country):

    data_json = {
	"query": {
		"codes": [
			"110009"
		],
		"country": "CZ"
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


    headers = { 
    "apikey": "zip_live_pWsWrXrfbOBJpOjUwXuVT8RDRkWCtUj44M2RKzLd"}

    params = (
    ("codes",codes),
    ("country",country),
    );

    # get reguest
    api_1 = requests.get(api_url, headers=headers, params=params,  verify=False).text
    
    f_data_json = json.loads(api_1)
    return f_data_json

# ================= App Scree ============================

st.write("# ZIP Code search:")
''
''
st.write("""
- API based 
- The information comes from https://app.zipcodestack.com/
""")

# ================== Rules for users ======================


with st.expander("How to use this function",
    icon=":material/help:"
    ):
    ''
    ''
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
    st.image("Pictures/Function_6/F6_menu_post_multiple.svg")
    ''
    st.caption("** This approach of multiple inputs in one request helps to save/limit the number of API calls (source application limits this)")


    ''
    ''
    st.write("Negative scenarios:")
    st.write("- In case that your ZIP code input (one) is **NOT** related to the CZ or SK country warning note will be displayed ")
    st.image("Pictures/Function_6/F6_menu_nozip.svg")
    st.write("- In case that your ZIP code is **NOT** related to the CZ or SK, but you provided multiple codes, then the exiting will be delivered the others not. E.g. 4 codes filled in (3 existing, 1 not) -> 3 will be delivered")

with st.expander("Some example of ZIP codes you can use",
    icon=":material/help:"
    ):
    st.write("""
    - CZ
        - 3 ZIP codes
        - 11000,25163,15800
    """
    )

    st.write("""
    - SK
        - 3 ZIP codes
        - 013 41,013 06,811 08 
    """
    )

# ================== User inputs ==========================

''
''
''
with st.form("Ahoj"):
    country = st.selectbox("Country:",
        ["CZ", "SK"],
        )
    
    codes = st.text_input("ZIP code")
    
    ''
    ''
    if st.form_submit_button(
        label="Submit",
        use_container_width=True,
        icon = ":material/apps:",
        ):

        # Function
        # f_data_json = get_request(codes, country)

        # For testing purposes 
        f_data_json = TEST_get_request(codes, country)
        # st.write(f_data_json)


        # ============ Data parsing from JSON ================


        # ==== Parsing of the ZIP codes from JSON =======
        # Those are the same ZIP CODES as entered in user input 
        # But in case that user will put a ZIP code which is not existing on the API side -> this mechanism will prevent from failing and just simply, will not get any response to show from the API. 

        # the JSON structure is build on dynamic value principle in segment 
        # "results": { "11000": [{}],"12300": [{}]}   - the numbers (in string type) are the dynamic ones -> yes, those are the inputs from user -> JSON reflects that in the message

        # step 1 - the dynamic values to be parsed into list
        result_val = []
        for result_jsn in f_data_json["results"]:
            result_jsn = str(result_jsn)
            result_val.append(result_jsn)
            
            #mapping into string
            result_val = list(map(str, result_val))
            # st.write(result_val)

        # step 2 - number of items in the list 
        a = len(result_val)

        # step 3 - the number of items - 1 => we get number of indexes 
        a = a - 1
        # st.write(a)

        if a == -1:
            st.warning("Your ZIP code(s) is not related to the selected country or doesn't exist in DB")
        
        else:
            pass

        # step 4 - setting a default index for for loop as O (to take the first dynamic number from the list as variable)
        index = 0

        # step 5 - while loop - to run until all the indexes checked/run
        while index <= a:

            # parsing of other values on the another JSON level 
            # the dynamic value are run based on the index number 
            result_val_single = result_val[index]

            for result in f_data_json["results"][result_val_single]:
                st.write(f"- ZIP code: {result['postal_code']}")
                st.write(f"- City name: {result['city_en']}")
                st.write(f"- State: {result['state_en']}")
                st.write(f"=====================================")
            
            # this increases the index number/move to the next item in the list
            index = index + 1