import streamlit as st
import pandas as pd
import math
import datetime
import requests
import json



tranport_types_list = ['Truck','Train','Airplane']

# Price per 1t/per approx 30km (one square on map)

#STANDAR - DELIVERY SERVICE
truck_kc = 689
train_kc = 230
plane_kc = 150_000

truck_eur = 27
train_eur = 10
plane_eur = 6250

list_kc_standard_default = [truck_kc, train_kc, plane_kc]
list_eur_standard_default = [truck_eur, train_eur, plane_eur]

# extra time for load unload and other admin stuff (in hours -> day)
#STANDAR - DELIVERY SERVICE
extra_time_truck_h = 32
extra_time_train_h = 48
extra_time_air_h = 72

express_extra_time_truck_h = 6
express_extra_time_train_h = 10
express_extra_time_air_h = 2

slow_extra_time_truck_h = 120
slow_extra_time_train_h = 120
slow_extra_time_air_h = 240


extra_time_df = pd.DataFrame({
    "Transport" : tranport_types_list,
    "Express" : [express_extra_time_truck_h,express_extra_time_train_h, express_extra_time_air_h],
    "Standard" : [extra_time_truck_h,extra_time_train_h, extra_time_air_h],
    "Slow" : [slow_extra_time_truck_h,slow_extra_time_train_h, slow_extra_time_air_h]
})

standard_def_kc_df = pd.DataFrame({
    "Transport" : tranport_types_list,
    "Default": list_kc_standard_default,
    "Currency": "Koruna"
})

standard_def_kc_df = standard_def_kc_df.style.format({
    "Default": "{:,.2f}"
})


standard_def_eur_df = pd.DataFrame({
    "Transport" : tranport_types_list,
    "Default": list_eur_standard_default,
    "Currency": "euro"
})

standard_def_eur_df = standard_def_eur_df.style.format({
    "Default": "{:,.2f}"
})

# PRICE Coeficients increasing(Express delivery) or decreasign (Slow delivery) price per square 
coef_truck = 0.4
coef_train = 0.5 
coef_air = 0.1


dataset_test = ({
"cz" : {
    "Prague" : {"big" : ["2","3"], "small" : ["6","7"], "train":"y", "air":"y"},
    "Brno" : {"big" : ["4","5"], "small" : ["10","13"], "train":"y", "air":"y"},
    "Olomouc" : {"big" : ["3","5"], "small" : ["8","15"], "train":"n", "air":"n"},
    "Plzen" : {"big" : ["3","2"], "small" : ["7","4"], "train":"n", "air":"n"},
    "Tabor" : {"big" : ["3","3"], "small" : ["9","8"], "train":"n", "air":"n"},
    "Ostrava" : {"big" : ["3","6"], "small" : ["7","18"], "train":"y", "air":"n"},
    "Liberec" : {"big" : ["1","3"], "small" : ["3","9"], "train":"n", "air":"n"},
    "Hradec Kralove" : {"big" : ["2","4"], "small" : ["5","11"], "train":"n", "air":"n"},
    "Pardubice" : {"big" : ["2","4"], "small" : ["6","11"], "train":"y", "air":"y"},
    "Zlin" : {"big" : ["3","6"], "small" : ["9","16"], "train":"n", "air":"n"},
    "Chomutov" : {"big" : ["2","2"], "small" : ["4","4"], "train":"n", "air":"n"},
    "Ceske Budejovice" : {"big" : ["4","3"], "small" : ["10","7"], "train":"n", "air":"n"},
    "Teplice" : {"big" : ["2","2"], "small" : ["4","6"], "train":"n", "air":"n"},
    "Most" : {"big" : ["2","2"], "small" : ["4","5"], "train":"y", "air":"n"},
    "Karlovy Vary" : {"big" : ["2","1"], "small" : ["5","3"], "train":"n", "air":"n"},
    "Kolin" : {"big" : ["2","3"], "small" : ["6","9"], "train":"y", "air":"n"},
    "Ceska Trebova" : {"big" : ["3","5"], "small" : ["7","13"], "train":"y", "air":"n"},
    "Jihlava" : {"big" : ["3","4"], "small" : ["9","10"], "train":"n", "air":"n"},
    "Pisek" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"n"},
},
"sk" : {
	"Bratislava" : {"big" : ["5","5"], "small" : ["14","14"], "train":"y", "air":"y"},
    "Kosice" : {"big" : ["4","9"], "small" : ["12","27"], "train":"y", "air":"y"},
    "Banska Bystrica" : {"big" : ["4","7"], "small" : ["12","21"], "train":"n", "air":"n"},
    "Zilina" : {"big" : ["3","7"], "small" : ["9","19"], "train":"y", "air":"n"},	
    "Presov" : {"big" : ["4","9"], "small" : ["10","27"], "train":"n", "air":"n"},	
    "Trnava" : {"big" : ["5","6"], "small" : ["14","17"], "train":"y", "air":"n"},	
    "Trencin" : {"big" : ["4","6"], "small" : ["11","17"], "train":"n", "air":"n"},	
    "Poprad" : {"big" : ["4","8"], "small" : ["10","24"], "train":"y", "air":"n"},	
    "Banska Stiavnica" : {"big" : ["5","7"], "small" : ["13","20"], "train":"n", "air":"n"},		
}
})

# //////////////////// API ///////////////////////

def api_get_rate():
    try:
        # api_freecurrency_api = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_wD1NduThhBnySFJAlV9f6xnQmMhkJa6qFzX7DJz4&currencies=EUR%2CCZK"

        #get reguest
        @st.cache_data(ttl=3600)
        def get_response_api(api_freecurrency_api):
            api_1 = requests.get(api_freecurrency_api, verify=False, timeout=5).text
            return api_1

        api_1 = get_response_api(api_freecurrency_api)


        # JSON format creation
        api_1_json = json.loads(api_1)


        # Search for data in the API defined format - JSON
        usd_to_czk_rate = api_1_json['data']['CZK']
        usd_to_czk_rate = round(usd_to_czk_rate, 2)

        usd_to_eur_rate = api_1_json['data']['EUR']
        usd_to_eur_rate = round(usd_to_eur_rate, 2)

        return  usd_to_czk_rate, usd_to_eur_rate

    except:
        st.warning("""
        - Apologies, API refused to make a connection. So to see the function, there are predefined values for the currency exchange rate.
        """
    )

        usd_to_czk_rate = 24.89
        usd_to_eur_rate = 0.87
        
        return usd_to_czk_rate, usd_to_eur_rate 



usd_to_czk_rate, usd_to_eur_rate = api_get_rate()


# Change of price based on rate - % in percantage decrease/increase

crit_1_kc = -9.3
crit_2_kc = -4.7
crit_3_kc = 0       # default range - crit_3_kc
crit_4_kc = 4.7

crit_1_eur = -5.9
crit_2_eur  = 0   # default range - crit_2_eur
crit_3_eur = 3.5 
crit_4_eur = 7.1


crit_1_kc_cond = " x < 20 "
crit_2_kc_cond = " 20 ≤ x < 21 "
crit_3_kc_cond = " 21 ≤ x < 22 "
crit_4_kc_cond = " 22 ≤ x "

crit_1_eur_cond = " x < 0.82 "
crit_2_eur_cond = " 0.82 ≤ x < 0.87 "
crit_3_eur_cond = " 0.87 ≤ x < 0.90 "
crit_4_eur_cond = " 0.90 ≤ x "

list_crit_kc = crit_1_kc, crit_2_kc, crit_3_kc, crit_4_kc

list_crit_eur = crit_1_eur, crit_2_eur, crit_3_eur, crit_4_eur


def increase_decrease(list):

    list_impact = []
    for item in list:
        if item < 0:
            result = 'cost decrease'
            list_impact.append(result)
        
        elif item == 0:
            result = 'default value'
            list_impact.append(result)

        elif item > 0:
            result = 'cost increase'
            list_impact.append(result)
        
        else:
            print("Issue - not scenario not covered in this def function")

    return list_impact


list_crit_kc_text = increase_decrease(list_crit_kc)
list_crit_eur_text = increase_decrease(list_crit_eur)




crit_dataset_kc = pd.DataFrame ({
    "Rule" : [crit_1_kc_cond, crit_2_kc_cond, crit_3_kc_cond, crit_4_kc_cond],
    "Impact (%)" : [crit_1_kc, crit_2_kc, crit_3_kc, crit_4_kc],
    "Impact " : list_crit_kc_text,
},)


crit_dataset_eur = pd.DataFrame ({
    "Rule" : [crit_1_eur_cond, crit_2_eur_cond, crit_3_eur_cond, crit_4_eur_cond],
    "Impact (%)" : [crit_1_eur, crit_2_eur, crit_3_eur, crit_4_eur],
    "Impact " : list_crit_eur_text,
},)


def rate_change_kc(usd_to_czk_rate, truck_kc, train_kc, plane_kc):

    # st.write(f"ve funkci usd/czk: {usd_to_czk_rate}")
    # st.write(f"ve funkci truck: {truck_kc}")
    # st.write(f"ve funkci train: {train_kc}")
    # st.write(f"ve funkci air: {plane_kc}")
    # st.write(f"ve funkci crit 1: {crit_2_kc }")

    if usd_to_czk_rate < 20:
        truck_kc = round(truck_kc + (truck_kc / 100) * crit_1_kc,0)
        train_kc = round(train_kc + (train_kc / 100) * crit_1_kc, 0)
        plane_kc = round(plane_kc + (plane_kc / 100) * crit_1_kc, 0)

        return truck_kc, train_kc, plane_kc
    
    elif 20 <= usd_to_czk_rate < 21:
        # st.write("jsem ve 2")
        truck_kc = round(truck_kc + (truck_kc / 100) * crit_2_kc, 0)
        train_kc = round(train_kc + (train_kc / 100) * crit_2_kc, 0)
        plane_kc = round(plane_kc + (plane_kc / 100) * crit_2_kc, 0)

        return truck_kc, train_kc, plane_kc

    elif 21 <= usd_to_czk_rate < 22:
        # st.write("jsem ve 3")
        truck_kc = truck_kc
        train_kc = train_kc
        plane_kc = plane_kc

        return truck_kc, train_kc, plane_kc
    
    elif 22 <= usd_to_czk_rate:
        # st.write("jsem ve 4")
        truck_kc = round(truck_kc + (truck_kc / 100) * crit_4_kc, 0)
        train_kc = round(train_kc + (train_kc / 100) * crit_4_kc, 0)
        plane_kc = round(plane_kc + (plane_kc / 100) * crit_4_kc, 0)

        return truck_kc, train_kc, plane_kc


truck_kc, train_kc, plane_kc = rate_change_kc(usd_to_czk_rate, truck_kc, train_kc, plane_kc)


def rate_change_eur(usd_to_eur_rate, truck_eur, train_eur, plane_eur):

    if usd_to_eur_rate < 0.82:
        # st.write("jsem ve 1")
        truck_eur = round(truck_eur + (truck_eur / 100) * crit_1_eur, 2)
        train_eur = round(train_eur + (train_eur / 100) * crit_1_eur, 2)
        plane_eur = round(plane_eur + (plane_eur / 100) * crit_1_eur, 2)

        return truck_eur, train_eur, plane_eur
    
    elif 0.82 <= usd_to_eur_rate < 0.87:
        # st.write("jsem ve 2")
        truck_eur = truck_eur
        train_eur = train_eur
        plane_eur = plane_eur

        return truck_eur, train_eur, plane_eur

    elif 0.87 <= usd_to_eur_rate < 0.90:
        # st.write("jsem ve 3")
        truck_eur = round(truck_eur + (truck_eur / 100) * crit_3_eur,2)
        train_eur = round(train_eur  + (train_eur  / 100) * crit_3_eur,2)
        plane_eur = round(plane_eur + (plane_eur / 100) * crit_3_eur,2)

        return truck_eur, train_eur, plane_eur
    
    elif 0.90 <= usd_to_eur_rate:
        # st.write("jsem ve 4")
        truck_eur = round(truck_eur + (truck_eur / 100) * crit_4_eur, 2)
        train_eur  = round(train_eur  + (train_eur  / 100) * crit_4_eur, 2)
        plane_eur = round(plane_eur + (plane_eur / 100) * crit_4_eur, 2)

        return truck_eur, train_eur, plane_eur


truck_eur, train_eur, plane_eur = rate_change_eur(usd_to_eur_rate, truck_eur, train_eur, plane_eur)


# =======================================================================
# /////////    Data parsing  /////////////

# Trains YES - ONLY YES
train_cz = []
for item in dataset_test['cz']:
    l2 = dataset_test['cz'][item]
    l3 = dataset_test['cz'][item]['train']
    if l3 == 'y':
        train_cz.append(item)

train_sk = []
for item in dataset_test['sk']:
    l2 = dataset_test['sk'][item]
    l3 = dataset_test['sk'][item]['train']
    if l3 == 'y':
        train_sk.append(item)


# Airplanes - overview (including no) - FULL LIST
train_cz_yn = []
for item in dataset_test['cz']:
    l2 = dataset_test['cz'][item]
    l3 = dataset_test['cz'][item]['train']
    train_cz_yn.append(l3)

train_sk_yn = []
for item in dataset_test['sk']:
    l2 = dataset_test['sk'][item]
    l3 = dataset_test['sk'][item]['train']
    train_sk_yn.append(l3)

# Airplanes YES - ONLY YES

air_cz = []
for item in dataset_test['cz']:
    l2 = dataset_test['cz'][item]
    l3 = dataset_test['cz'][item]['air']
    if l3 == 'y':
        air_cz.append(item)

air_sk = []
for item in dataset_test['sk']:
    l2 = dataset_test['sk'][item]
    l3 = dataset_test['sk'][item]['air']
    if l3 == 'y':
        air_sk.append(item)

# Airplanes - overview (including no) - FULL LIST
air_cz_yn = []
for item in dataset_test['cz']:
    l2 = dataset_test['cz'][item]
    l3 = dataset_test['cz'][item]['air']
    air_cz_yn.append(l3)

air_sk_yn = []
for item in dataset_test['sk']:
    l2 = dataset_test['sk'][item]
    l3 = dataset_test['sk'][item]['air']
    air_sk_yn.append(l3)


# Function for change of data from original data object to have a meaning for visualization 
def text_output(list_input):

    output = []
    for i in list_input:
        if i == 'y':
            output.append('Available')
        if i == 'n':
            output.append('No')

    return output
       

train_cz_yn_text = text_output(train_cz_yn)
train_sk_yn_text = text_output(train_sk_yn)
air_cz_yn_text = text_output(air_cz_yn)
air_sk_yn_text = text_output(air_sk_yn)


# Names of cities 
list_cz_az = []
list_cz = []
for item in dataset_test['cz']:
    list_cz.append(item)
    list_cz_az.append(item)

# st.write(list_cz)

list_sk_az = []
list_sk = []
for item in dataset_test['sk']:
    list_sk.append(item)
    list_sk_az.append(item)


# st.write(list_sk)

# Sorting A-Z for select 

list_cz_az.sort()
list_sk_az.sort()

# Table overview - data set 

table_overview_full_cz = pd.DataFrame({
    "City" : list_cz,
    "Road" : 'Available',
    "Train" : train_cz_yn_text,
    "Airplane" : air_cz_yn_text
})

table_overview_full_cz.index +=1


table_overview_full_sk = pd.DataFrame({
    "City" : list_sk,
    "Road" : 'Available',
    "Train" : train_sk_yn_text,
    "Airplane" : air_sk_yn_text
})

table_overview_full_sk.index +=1

# //////////////////// Frontend screen - top part ////////////////////////

st.write("# Transport calculation")

''
''
''
''
st.image("Pictures/Function_7/F7_map_3.png")

''
''
with st.expander("City overview", icon = ":material/pin_drop:"):

    ''
    st.image("Pictures/Function_7/F7_map_cities.png")
    ''
    st.write("- **Czech Republic:**")
    st.dataframe(table_overview_full_cz)
    ''
    st.write("- **Slovakia:**")
    st.dataframe(table_overview_full_sk)

with st.expander("Currency and rate", icon = ":material/payments:"):

    ''
    ''
    col_r1,col_r2 = st.columns(2)

    col_r1.metric(label="USD to CZK", value= usd_to_czk_rate)

    col_r2.metric(label="USD to EUR", value= usd_to_eur_rate)

    ''
    st.write("- This is a **dynamic part** - API based")
    st.write("- **Exchange rate of the day** influences the costs/price within calculations")

    ''
    ''
    st.write("###### CZ - Czech Republic:")
    st.dataframe(crit_dataset_kc, hide_index=True)
    ''

    st.write("Overview:")
    st.write("""
             - The 0% change / default values (Rate: 21 <= x < 22 ) 
                - For 1 calculation/distance unit 
                - For **Standard** delivery
             - These values are also used for the calculation:
                - of % difference in case of rate in differnet range
                - for different speed of delivery (Express, Slow)
             """)
    col_r3,col_r4 = st.columns(2)
    col_r3.dataframe(standard_def_kc_df, hide_index=True, use_container_width=True)


    ''
    st.write("###### SK - Slovakia:")
    st.dataframe(crit_dataset_eur, hide_index=True)
    ''

    st.write("Overview:")
    st.write("""
             - The 0% change / default values (Rate:  0.82 <= x < 0.87 ) 
                - For 1 calculation/distance unit 
                - For **Standard** delivery
             - These values are also used for the calculation:
                - of % difference in case of rate in differnet range
                - for different speed of delivery (Express, Slow)
             """)
    col_r3,col_r4 = st.columns(2)
    col_r3.dataframe(standard_def_eur_df, hide_index=True, use_container_width=True)

# /////////////////////////////////////////////////////////////////////////
def price_decision(selected_currency, selected_transport):

    if selected_currency == 'koruna':
        if selected_transport == 'Truck':
            price_square = truck_kc
            return price_square
        
        if selected_transport == 'Train':
            price_square = train_kc
            return price_square

        if selected_transport == 'Airplane':
            price_square = plane_kc
            return price_square
    

    if selected_currency == 'euro':
        if selected_transport == 'Truck':
            price_square = truck_eur
            return price_square
        
        if selected_transport == 'Train':
            price_square = train_eur
            return price_square

        if selected_transport == 'Airplane':
            price_square = plane_eur
            return price_square




# list_cz = []
# for item in dataset_test['cz']:
#     list_cz.append(item)

# # st.write(list_cz)


# list_sk = []
# for item in dataset_test['sk']:
#     list_sk.append(item)


# # st.write(list_sk)



# Filters 
''
''
''


col1,col2 = st.columns(2, gap="large")


radio_from_country = col1.radio(
    "Country from:",
    options=["CZ","SK"],
)

radio_from_country = radio_from_country.lower()

if radio_from_country == "cz":
    
    from_city = col1.selectbox("City from:", list_cz_az)

if radio_from_country == "sk":

    from_city = col1.selectbox("City from:", list_sk_az)





radio_to_country = col2.radio(
    "Country to:",
    options=["CZ","SK"]
)

radio_to_country = radio_to_country.lower()

if radio_to_country == "cz":
    
    to_city = col2.selectbox("City to:", list_cz_az)

if radio_to_country == "sk":

    to_city = col2.selectbox("City to:", list_sk_az)




# function for offering relevant currency to choose from in case that international transport CZ <-> SK
def offer_currency(radio_from_country,radio_to_country):

    if radio_from_country == 'sk' and radio_to_country == 'sk':
        currency = 'euro'
        return currency
    
    elif radio_from_country == 'cz' and radio_to_country == 'cz':
        currency = 'koruna'
        return currency
    
    else:
        currency = ['koruna', 'euro']
        return currency

currency = offer_currency(radio_from_country,radio_to_country)


''
''
''
selected_currency = st.radio(
    "Currency:",
    currency
)




#train / truck / plaine

def train_available(dataset_test, radio_from_country, radio_to_country, from_city,to_city):

	train_from = dataset_test[radio_from_country][from_city]['train']
	train_to = dataset_test[radio_to_country][to_city]['train']
         
	return train_from, train_to


train_from, train_to = train_available(dataset_test,radio_from_country, radio_to_country, from_city,to_city)


def options_train_result(train_from, train_to):
    
    if train_from == 'y' and train_to == 'y':
        train_result = ['Truck','Train']
    else:
        train_result = ['Truck']
        
    return train_result

train_result = options_train_result(train_from, train_to)



def aircraft_available(dataset_test, radio_from_country, radio_to_country, from_city,to_city):

	air_from = dataset_test[radio_from_country][from_city]['air']
	air_to = dataset_test[radio_to_country][to_city]['air']
         
	return air_from, air_to


air_from, air_to = aircraft_available(dataset_test,radio_from_country, radio_to_country, from_city,to_city)


def options_air_result(air_from, air_to):
    
    if air_from == 'y' and air_to == 'y':
        train_result = ['Airplane']
    else:
        train_result = []
        
    return train_result

air_result = options_air_result(air_from, air_to)



transport_options_list = train_result + air_result
''
selected_transport = st.radio("Transport type:", transport_options_list)

# //////////////// Price per square, based on selected transport  ///////
price_square = price_decision(selected_currency,selected_transport)

''

with st.expander("Transport type comparison", icon=":material/info:"):

    ''
    st.write("""
             - There is few factors to consider:
                - Time, Costs
                - Type of Cargo 
                - Infrasture availability  
             
             """)

    ''
    st.image("Pictures/Function_7/F7_transport_comparison_table.svg")


with st.expander("Truck / Road", icon=":material/local_shipping:"):

    ''
    st.write("""- Every city is available -> no restrictions""")
    st.write("""- But the driver needs mandatory breaks which can prolong the journey/delivery time""")


    ''
    st.write("###### Mandatory breaks:")

    st.write("""
             - The cargo can be impacted by **mandatory breaks for the driver**
             - This also **influences the time of the delivery**
             """)
    
    st.write("""
             - **Rules/law**:
                - A driver can drive **4.5 hours** and then needs to take a **mandatory 45 minutes break**
                - A driver can drive for **9 hours a day** max.   
                - After the 9 hours mandatory **10 hours break** before continuing to drive 
                - **Exception:** in case that the distance is **within 10 hours** of driving, exception can be made                        
             """)

    ''
    st.write(" -> Distance is **not** longer than **4.5 hours** - no mandatory break")
    st.write(" -> Distance is **longer** than **4.5 hours** - mandatory **45 minutes** break")
    st.write(" -> Distance is **not** longer than **9 hours** - mandatory **45 minutes** break")
    st.write(" -> Distance is **not** longer than **10 hours** (exception) - mandatory **2x  45 minutes** break")
    st.write(" -> In case that the distance is longer than **9 and 10 hours** (10+) - there is **45 minutes** break + **10 hours** break")
    
    ''
    st.caption("""
               * Example of journey between 9 - 10 hours -> the exception: Karlovy Vary (CZ) - Poprad (SK)
               * Example of journey longer than 9 or 10 hours with 10 hours sleep break: Teplice (CZ) - Kosice (SK) or Karlovy Vary (CZ) - Kosice (SK)
                """)



with st.expander("Train / Rails", icon=":material/train:"):

    ''
    st.write("""
    -   Train does **not need breaks** for the driver (in comparison with Truck)
        - The transport planning includes also **change of the drivers**, if it is that long
        - Train jurney is **not** inturupted by mandtory breaks  
    """)

    st.write("""- But is **less flexible** - Only some cities connected by rails""")
    ''
    st.image("Pictures/Function_7/F7_map_trains.png")

    data_table_train_cz = pd.DataFrame({
        "City CZ" : train_cz
        })
    

    data_table_train_sk = pd.DataFrame({
        "City SK" : train_sk
        })
    
    data_table_train_cz.index += 1
    data_table_train_sk.index += 1

    ''
    st.dataframe(data_table_train_cz)
    ''
    st.dataframe(data_table_train_sk)

with st.expander("Airplane", icon=":material/travel:"):
    ''
    st.write("""- Very expensive but fast -> Benficial for time critical goods/transports""")
    st.write("""- Only some cities connected""")
    ''
    st.image("Pictures/Function_7/F7_map_air.png")

    data_table_air_cz = pd.DataFrame({
        "City CZ" : air_cz
        })
    

    data_table_air_sk = pd.DataFrame({
        "City SK" : air_sk
        })
    
    data_table_air_cz.index += 1
    data_table_air_sk.index += 1

    ''
    st.dataframe(data_table_air_cz)
    ''
    st.dataframe(data_table_air_sk)


# Radio - urgency input
urgency_offer = ['Express', 'Standard', 'Slow']

''
''
urgency = st.radio("Delivery service:", urgency_offer, index=1, captions=[
        "Fast administration process -> delivery as soon as possible",
        "Within 2-3 days cargo should be ready to go",
        "5-10 days to get cargo ready to go ",
    ],)

''
''
with st.expander("**SLA** - Service Level Agreement (Express, Standard, Slow)", icon= ":material/contract:"):

    ''
    st.write(" - **Time** - Cargo on its way till this time - **HOURS**")
    st.dataframe(extra_time_df, hide_index=True)




def change_express(price_square, selected_transport):

    if selected_transport == 'Truck':
        price_square = price_square + (price_square * coef_truck)
        return price_square
    
    elif selected_transport == 'Train':
        price_square = price_square + (price_square * coef_train)
        return price_square
    
    elif selected_transport == 'Airplane':
        price_square = price_square + (price_square * (7*coef_air))
        return price_square

def change_slow(price_square, selected_transport):

    if selected_transport == 'Truck':
        price_square = price_square - (price_square * coef_truck)
        return price_square
    
    elif selected_transport == 'Train':
        price_square = price_square - (price_square * coef_train)
        return price_square
    
    elif selected_transport == 'Airplane':
        price_square = price_square - (price_square * coef_air)
        return price_square



if urgency  == 'Express':
    price_square = change_express(price_square, selected_transport)


if urgency  == 'Slow':
    price_square = change_slow(price_square, selected_transport)



def extra_time_decision(urgency, selected_transport, extra_time_truck_h, extra_time_train_h, extra_time_air_h):

    if urgency == 'Slow':
        if selected_transport == 'Truck':
            extra_time = slow_extra_time_truck_h
            return extra_time
        
        elif selected_transport == 'Train':
            extra_time = slow_extra_time_train_h 
            return extra_time
        
        elif selected_transport == 'Airplane':
            extra_time = slow_extra_time_air_h 
            return extra_time

    if urgency == 'Standard':
        if selected_transport == 'Truck':
            extra_time = extra_time_truck_h
            return extra_time
        
        elif selected_transport == 'Train':
            extra_time = extra_time_train_h
            return extra_time
        
        elif selected_transport == 'Airplane':
            extra_time = extra_time_air_h
            return extra_time

    if urgency == 'Express':
        if selected_transport == 'Truck':
            extra_time = express_extra_time_truck_h 
            return extra_time
        
        elif selected_transport == 'Train':
            extra_time = express_extra_time_train_h
            return extra_time
        
        elif selected_transport == 'Airplane':
            extra_time = express_extra_time_air_h
            return extra_time
    


extra_time = extra_time_decision(urgency, selected_transport, extra_time_truck_h, extra_time_train_h, extra_time_air_h)




if urgency == 'Express' or urgency == 'Standard':
    
    str_extra_time = str(extra_time)
    extra_time_vizualization = (str_extra_time + " " + "hours")


if urgency == 'Slow':
    extra_time_callc = extra_time / 24
    extra_time_callc = int(extra_time_callc)
    extra_time_callc = str(extra_time_callc)
    extra_time_vizualization = (extra_time_callc + " " + "days")



''
st.write(f" - **{selected_transport}** - **{urgency}** -> the cargo can be on its way in **{extra_time_vizualization}**.")

st.write(f" - Unit price for distance calculation: **{price_square:,.2f} {selected_currency}**")



# Expanders
''
with st.expander("Unit price", icon= ":material/info:"):

    ''
    st.write("- Is a price per specific distance")
    st.write("- The function/calculation works based on **coordinate system**")
    st.write("- Unit means specific field in this coordinate system")
    st.write("- **Based on the units, distance and price is calculated**")
    st.write("- **1 unit is approximatelly ~ 30 km** (but not always - there are some variables/coeficients making calculation corrections, dependings on case City A to City B )")
    st.write("- If the distance is **less than** ~ 30 km (You travel within 1 unit), the final price is calculated as 1 unit. This also helps to keep profit for the business.  Example: Teplice <-> Most")

''
''
st.write("**Extra services:**")

col_ch_1, col_ch_2, col_ch_3 = st.columns(3)

check_isurance = col_ch_1.checkbox("Insurance extra")

check_fragile = col_ch_2.checkbox("Fragile goods")

if selected_transport == 'Airplane':
    check_danger = col_ch_3.checkbox("Danger goods", disabled= True)
    col_ch_3.caption("*Not allowed in aircraft")

else:
    check_danger = col_ch_3.checkbox("Danger goods")


#determintation of value/option
if selected_currency == 'koruna':
    step_defined = 50_000
    min_value = 50_000
    max_value = 25_000_000
    help_info = ("""
        - Type a value of your shipment. It will be used for calculation. 
        - Min value 50 000 koruna
        - Max value 25 000 000 koruna
        """)


if selected_currency == 'euro':
    step_defined = 10_000
    min_value = 5_000
    max_value = 1_000_000
    help_info = ("""
            - Type a value of your shipment. It will be used for calculation. 
            - Min value: 5 000 euro
            - Max value: 1 000 000 euro
            """)


if check_isurance or check_fragile or check_danger is True:
    ''
    shipment_value = st.number_input(
        label=f"Shipment value - currency: **{selected_currency}**",
        value=None,
        placeholder="Type shipment value",
        min_value= min_value,
        max_value= max_value,
        # step = step_defined,
        help = help_info
        )
    
    if shipment_value == None:
        st.warning("Please insert shipment value")

else:
    shipment_value = None


''
with st.expander("Extra services - Overview", icon= ":material/info:"):

    ''
    st.write("""
    - Multiple choices can be selected
    - Note: **Airplane** - Danger goods is **not allowed**
    """)

    ''
    st.write("""
    - Costs:
        - Insurance extra -> **10%** from shipment value
        - Fragile goods -> **5%** from shipment value
        - Danger goods -> **7%** from shipment value
    """)

    st.image("Pictures/Function_7/F7_table_shipment_value.svg")

with st.expander("Fragile goods", icon= ":material/quick_reference:"):

    ''
    st.write("""
    - Overview of goods and the common type of transport
    """)

    st.image("Pictures/Function_7/F7_table_fragile_truck_train.svg")
    st.image("Pictures/Function_7/F7_table_fragile_airplane.svg")

with st.expander("Danger goods", icon= ":material/warning:"):

    ''
    st.write("""
    - Overview of goods and the common type of transport
    - Note: **Airplane** - Danger goods is **not allowed**
    """)

    st.image("Pictures/Function_7/F7_table_danger_truck_train.svg")



''
''
st.write("**Delivery specification - Door-to-Door:**")
st.write(f"From city ({from_city}):")

# input validati / warning
def more_true(list_bool):
   
    list_bool_result=[]

    for item in list_bool:
        if item == True:
            item = 1
            list_bool_result.append(item)
        

        if item == False:
            item = 0
            list_bool_result.append(item)
    
    sumary = sum(list_bool_result)
    return sumary


col_ch2_1, col_ch2_2, col_ch2_3 = st.columns(3)

if selected_transport == 'Truck':
    check_delivery_not_f = col_ch2_1.checkbox("Within city", key='city_1', value = True)

    check_delivery_10_f = col_ch2_2.checkbox("10 km", key='10km_1')

    check_delivery_20_f = col_ch2_3.checkbox("20 km", key='20km_1')


    checkbox_list_from = [check_delivery_not_f, check_delivery_10_f, check_delivery_20_f]

    sumary_from = more_true(checkbox_list_from)

    if sumary_from == 0:
        st.warning("Select one option")

    if sumary_from > 1:
        st.warning("Only one option can be selected")
    


if selected_transport == 'Airplane' or selected_transport == 'Train':
    check_delivery_not_at_f = col_ch2_1.checkbox("No", key='city_2', value = True)

    check_delivery_10_at_f  = col_ch2_2.checkbox("10 km", key='10km_2')

    check_delivery_20_at_f  = col_ch2_3.checkbox("20 km", key='20km_2')


    checkbox_list_from = [check_delivery_not_at_f, check_delivery_10_at_f, check_delivery_20_at_f]

    sumary_from = more_true(checkbox_list_from)

    if sumary_from == 0:
        st.warning("Select one option")

    if sumary_from > 1:
        st.warning("Only one option can be selected")

''

st.write(f"To city: ({to_city}):")

col_ch3_1, col_ch3_2, col_ch3_3 = st.columns(3)

if selected_transport == 'Truck':
    check_delivery_not_t = col_ch3_1.checkbox("Within city",key='city_3', value = True)

    check_delivery_10_t = col_ch3_2.checkbox("10 km", key='10km_3')

    check_delivery_20_t = col_ch3_3.checkbox("20 km", key='20km_3')

    checkbox_list_to = [check_delivery_not_t, check_delivery_10_t, check_delivery_20_t]

    sumary_to = more_true(checkbox_list_to)

    if sumary_to == 0:
        st.warning("Select one option")

    if sumary_to > 1:
        st.warning("Only one option can be selected")



if selected_transport == 'Airplane' or selected_transport == 'Train':

    check_delivery_not_at_t = col_ch3_1.checkbox("No",key='city_4', value = True)

    check_delivery_10_at_t = col_ch3_2.checkbox("10 km", key='10km_4')

    check_delivery_20_at_t  = col_ch3_3.checkbox("20 km", key='20km_4')

    checkbox_list_to = [check_delivery_not_at_t , check_delivery_10_at_t , check_delivery_20_at_t]


    sumary_to = more_true(checkbox_list_to)

    if sumary_to == 0:
        st.warning("Select one option")

    if sumary_to > 1:
        st.warning("Only one option can be selected")


''
with st.expander("Door-to-Door", icon= ":material/info:"):

    ''
    st.write("""
    - **The point of Door-to-Door is to define whether:**
        - The transport between cities will be just from City A to City B **configured upper**
        - Or eventually from/to somewhere else within defined areas (City, ~ 10km, ~20km)
    """)

    ''
    st.write(""" 
    - **Truck:**
        - **City** - everywhere within City area **for free**
        - **10 km** radius - **500 koruna** ; **20 euro**
        - **20 km** radius - **1 000 koruna** ; **40 euro**
    """)

    ''
    st.write(""" 
    - **Train and Airplane:**
        - Measured from Train Station or Airport
        - **Higher price** due to need of **truck** and **Shipmant transfer**
        - **No** - pick up/delivery just from/to Train Station/Airport by Train/Airplane
        - **10 km** radius - **1 000 koruna** ; **40 euro**
        - **20 km** radius - **1 500 koruna** ; **60 euro**
    """)


    ''
    st.write("- **More details**:")

    st.link_button(
                label = "Go to Door-to-Door page",
                url="https://dataparsing.streamlit.app/F7_FUNCTION_transport",
                help="The button will redirect to the relevant page within this app for download.",
                use_container_width=True,
                icon=":material/launch:"
            )


    ''
    ''
    st.write("###### Simple view/example:")

    st.image("Pictures/Function_7/Function_7_F7_dtd_legend_small_2.svg", width= 350)

    ''
    st.image("Pictures/Function_7/F7_dtd_transport_abb_air.svg")

    ''
    st.write(""" 
    - Selected transport between **A** and **B** - **Airplane**
    - Service **ordered** just from the **A** point ('From city') - **Airport**
    - Delivery to **B** point ('To' city) - **Airport**, but customer pays extra delivery to point **B in the area of 20km**
    """)
    st.write(""" 
    - Result:
        -  Customer will deliver the Shipment to point **A** (Airport) **on his own**
        - **A** to **B** distance (Airport to Airport) will be provided by our company (Airplane)
        - Customer pays for delivery to **B - 20km** -> our company will make a shipament transfer from **Airplane to Truck** for the last **20 km**     
    """)




# Check box validation /transformation to money

def check_box_money_extra_services(shipment_value, check_isurance, check_fragile, check_danger):

    insurance = 10
    fragile = 5
    danger = 7


    if check_isurance == True:
        money_insurance = shipment_value / 100 * insurance
    else:
        money_insurance = 0

    if check_fragile == True:
        money_fragile = shipment_value / 100 * fragile
    
    else:
        money_fragile = 0

    if check_danger == True:
        money_danger = shipment_value / 100 * danger
    
    else:
        money_danger = 0

    return money_insurance, money_fragile, money_danger


# In case that any of extra services (insurance, fragile, danger) required. This condition allows to make a calculation, if not. it will be skipped. In case is required but the value of shipment is 'None' (not entered or forgoten), there is validation after submit button. 

if shipment_value is not None:

    money_insurance, money_fragile, money_danger = check_box_money_extra_services(shipment_value,check_isurance, check_fragile, check_danger)




# //////////////// Submit button ////////////////////


''
st.write("------")
if st.button("Submit", use_container_width=True):

    # Firstly, validation if all inputs are provided properly
    def input_validation(from_city,to_city):
        if from_city == to_city:
            st.warning("City From and To is the same -> They need to be different")
            st.stop()
        
        else:
            pass

    input_validation(from_city,to_city)


    if sumary_from > 1 or sumary_to > 1:
        st.warning("More than 1 option has been selected in Door-to-Door section. Please select just one.")
        st.stop()

    if sumary_from == 0 or sumary_to == 0:
        st.warning("Missing select in Door-to-Door section. Please select one.")
        st.stop()
    
    if (check_isurance or check_fragile or check_danger is True) and shipment_value == None:
        st.warning("You didn't provide Shipment value. Please go up and provide.")
        st.stop()  



    if check_isurance is False  and check_fragile is False and check_danger is False:

        money_insurance = 0
        money_fragile = 0
        money_danger = 0




    # Parsing fo calculation
    def pars_from_city(from_city, dataset_test):
        
        from_big = dataset_test[radio_from_country][from_city]['big']

        from_small = dataset_test[radio_from_country][from_city]['small']

        return from_big, from_small

        
    def pars_to_city(to_city, dataset_test):
        
        to_big = dataset_test[radio_to_country][to_city]['big']
        to_small = dataset_test[radio_to_country][to_city]['small']

        return to_big, to_small



    from_big, from_small = pars_from_city(from_city, dataset_test)

    to_big, to_small = pars_to_city(to_city, dataset_test)



    def pars_from_big_small_rc(from_big, from_small):
        from_big_r = from_big[0]
        from_big_c = from_big[1]

        from_small_r = from_small[0]
        from_small_c = from_small[1]
        return from_big_r, from_big_c, from_small_r, from_small_c
    

    def pars_to_big_small_rc(to_big, to_small):
        to_big_r = to_big[0]
        to_big_c = to_big[1]

        to_small_r = to_small[0]
        to_small_c = to_small[1]
        return to_big_r, to_big_c, to_small_r, to_small_c
    



    from_big_r, from_big_c, from_small_r, from_small_c = pars_from_big_small_rc(from_big,from_small)

    to_big_r, to_big_c, to_small_r, to_small_c = pars_to_big_small_rc(to_big,to_small)

    # Data type change str -> int
    from_big_r = int(from_big_r)
    from_big_c = int(from_big_c)
    from_small_r = int(from_small_r)
    from_small_c = int(from_small_c)

    to_big_r = int(to_big_r)
    to_big_c = int(to_big_c)
    to_small_r = int(to_small_r)
    to_small_c = int(to_small_c)


    # st.write(f"after function from_big R: {from_big_r}, C: {from_big_c}")
    # st.write(f"after function from_small R: {from_small_r}, C: {from_small_c}")

    # st.write(f"after function to_big R: {to_big_r}, C: {to_big_c}")
    # st.write(f"after function to_small R: {to_small_r}, C: {to_small_c}")



    def calculation_L3B(small_result_r,small_result_c):
        # st.write("LEVEL 3B inside detail calculation - ELSE")
        # st.write(f"LEVEL 3B small result_r: {small_result_r}")
        # st.write(f"LEVEL 3B small result_c: {small_result_c}")

        #long diagonal distance compensation
        comp = small_result_r + small_result_c


        if comp < 8:
            calcul = (small_result_r + small_result_c - 1)
            price = calcul * price_square
            # st.write(f"LEVEL 3 if 1 - před navratem price: {price}")

            distance = calcul * 31.57
            return price, distance
        
        elif 8 <= comp < 10:
            calcul = (small_result_r + small_result_c - 2)
            price = calcul * price_square
            # st.write(f"LEVEL 3 if 2 - před navratem price: {price}")

            distance = calcul * 33.08 #musim upravit nemam testovaci vzorky
            return price, distance


        elif 10 <= comp < 13:
            calcul = (small_result_r + small_result_c - 2.5)
            price = calcul * price_square
            # st.write(f"LEVEL 3 if 3 -před navratem price: {price}")

            distance = calcul * 33.08   #musim upravit nemam testovaci vzorky
            return price, distance
        
        elif 13 <= comp < 16:
            calcul = (small_result_r + small_result_c - 4)
            price = calcul * price_square
            # st.write(f"LEVEL 3 if 4 -před navratem price: {price}")

            distance = calcul * 35.68
            return price, distance
        
        elif 16 <= comp < 18:
            calcul = (small_result_r + small_result_c - 5)
            price = calcul * price_square
            # st.write(f"LEVEL 3 if 5 -před navratem price: {price}")

            distance = calcul * 34.24
            return price, distance
        
        elif 18 <= comp:
            calcul = (small_result_r + small_result_c - 8)
            price = calcul * price_square
            # st.write(f"LEVEL 3 if 6 -před navratem price: {price}")

            distance = calcul * 36.75
            return price, distance



    #Calculation in case that move is on horizontal r=0 or vertical level c=0
    def calculation_L3A_R0C0(small_result_r, small_result_c):
        # st.write("LEVEL 3A_R0C0 inside detail calculation")
        # st.write(f"LEVEL 3A_R0C0 small_result_r: {small_result_r}")
        # st.write(f"LEVEL 3A_R0C0 small_result_c: {small_result_c}")

        if small_result_r == 0:
            price = small_result_c * price_square
            distance = small_result_c * 31.86
            return price, distance
        
        if small_result_c == 0:
            price = small_result_r * price_square
            distance = small_result_r * 31.86
            return price, distance


    # if different big region 
    def calculation_L2(from_small_r, to_small_r, from_small_c, to_small_c):
        # st.write("LEVEL 2 inside detail calculation")
        small_result_r = abs(from_small_r - to_small_r)
        small_result_c = abs(from_small_c - to_small_c)

        if small_result_r <= 1 and small_result_c <= 1:
            price = price_square
            return price, distance
        
        elif small_result_r == 0 or small_result_c == 0:
            price, distance = calculation_L3A_R0C0(small_result_r, small_result_c)
            return price, distance
        
        else:
            price, distance = calculation_L3B(small_result_r,small_result_c)
            return price, distance



    # if big R = C -> same price
    def calculation_L1(from_big_r, to_big_r,from_big_c, to_big_c, from_small_r,to_small_r, from_small_c, to_small_c):
        
        big_result_r = abs(from_big_r - to_big_r)
        big_result_c = abs(from_big_c - to_big_c)
        small_result_r = abs(from_small_r - to_small_r)
        small_result_c = abs(from_small_c - to_small_c)
        # st.write(f" LEVEL 1: big_result_r: {big_result_r}")
        # st.write(f" LEVEL 1: big_result_c: {big_result_c}")

        if (big_result_r == 0 and big_result_c == 0) and (small_result_r <= 1 and small_result_c <= 1):
            price = price_square
            distance = 24.15
            return price, distance

        else:
            # st.write("LEVEL 1: Else happened")
            price, distance = calculation_L2(from_small_r, to_small_r, from_small_c, to_small_c)
            return price, distance


    price, distance = calculation_L1(from_big_r, to_big_r, from_big_c, to_big_c,from_small_r, to_small_r,from_small_c, to_small_c)

 

    def calcul_delivery_time(distance,selected_transport):

        if selected_transport == 'Truck':
            time_journey = distance / 70
            # extra_time_h = extra_time_truck_h
            # return extra_time_h, time_journey 
            return time_journey 

        if selected_transport == 'Train':
            time_journey = distance / 80
            # extra_time_h = extra_time_train_h
            # return extra_time_h, time_journey 
            return time_journey 
        
        if selected_transport == 'Airplane':
            time_journey = distance / 700
            # extra_time_h = extra_time_air_h
            # return extra_time_h, time_journey 
            return time_journey 

    time_journey  = calcul_delivery_time(distance,selected_transport)



    # mandatory breaks for truck 

    def one_shift(time_journey):

        num_break = time_journey / 4.5    #mandatory break 
        
        if num_break <= 1:
            # 0 breaks needed -> 0.0 hour of break time
            result = 0
            return result
            
        elif 1 <= num_break <= 2:
            # 1 break needed -> 0.75 hour (45 minutues break after 4.5 hour of driving)
            result = 0.75
            return result

    def calcul_time_break(time_journey):

        # max 9 hours of driving a day 
        if time_journey <= 9:
            break_n = one_shift(time_journey)
            return break_n

        # Law alows to drive 10 hours and no longer (for journey between 9-10 hours)
        # 2 x 45 minutes break -> 1.5 hour
        if 9 < time_journey <= 10:
            break_n = 1.5
            return break_n
            
        elif time_journey > 10:

            shift_full = time_journey / 9

            # split of the number for calculation 
            y = math.modf(shift_full)
            decimal_shift = y[0]
            number_of_shifts = y[1]

            # cas v HODINACH kolik mi zaberou pauzy Z CELÝCH  9 smen
            time_breaks_h = (number_of_shifts * 45)/60  # 45 min (mandatory break)/60 => HOURS

            # Number of mandatory breaks after every 9 hours (10 hours sleep/break)
            # Example 18 hour journy -> 2x 9hour shift -> 1x 10 hour break in between
            # Example 27 hour journy -> 3x 9hour shift -> 2x 10 hour break in between
            if decimal_shift > 0.00:
                time_spent_sleep_breaks_h = (number_of_shifts) * 10

            if decimal_shift == 0.00:
                time_spent_sleep_breaks_h = (number_of_shifts - 1) * 10
                
            # All the other hours in between the "full number of 9 hours" is covered here by "decimals" of hours indicating mandatory 45 minut break aftre 4.5 hours of driving (9 hours = 1.0 -> 4.5 hours = 0.5)
            if decimal_shift < 0.5:
                decimal_break = 0
            
            if 0.5 <= decimal_shift < 1:
                decimal_break = 1
            
            if decimal_shift > 1:
                st.write("error in calculation")

            # cas v HODINACH kolik mi zaberou pauzy v rámci decimalni hodnoty (45 minut/60) = hodiny
            decimal_time_h = (decimal_break * 45)/60

            final_time_breaks = time_breaks_h + time_spent_sleep_breaks_h + decimal_time_h
            return final_time_breaks


    if selected_transport == 'Truck':
        time_break = calcul_time_break(time_journey)


    # Door-to-Door inputs -> transformation to costs

    if selected_currency == 'euro':
        def door_to_door_eur(list_bool, selected_transport):
            
            if selected_transport == 'Truck':
                if list_bool[0] == True:
                    result = 0
                    return result

                if list_bool[1] == True:
                    result = 20
                    return result
                
                if list_bool[2] == True:
                    result = 40
                    return result

            if selected_transport == 'Train' or selected_transport == 'Airplane':

                if list_bool[0] == True:
                    result = 0
                    return result

                if list_bool[1] == True:
                    result = 40
                    return result
                
                if list_bool[2] == True:
                    result = 60
                    return result


        
        door_to_result = door_to_door_eur(checkbox_list_to, selected_transport)
        door_from_result = door_to_door_eur(checkbox_list_from, selected_transport)


    if selected_currency == 'koruna':
        def door_to_door_koruna(list_bool, selected_transport):
            
            if selected_transport == 'Truck':
                if list_bool[0] == True:
                    result = 0
                    return result

                if list_bool[1] == True:
                    result = 500
                    return result
                
                if list_bool[2] == True:
                    result = 1000
                    return result

            if selected_transport == 'Train' or selected_transport == 'Airplane':

                if list_bool[0] == True:
                    result = 0
                    return result

                if list_bool[1] == True:
                    result = 1000
                    return result
                
                if list_bool[2] == True:
                    result = 1500
                    return result


        
        door_to_result = door_to_door_koruna(checkbox_list_to, selected_transport)
        door_from_result = door_to_door_koruna(checkbox_list_from, selected_transport)


    def dtd_distance(list_bool):
        
        if list_bool[0] == True:
            result = 0
            return result

        if list_bool[1] == True:
            result = 10
            return result
        
        if list_bool[2] == True:
            result = 20
            return result


    

    from_city_extra_doortdoor = dtd_distance(checkbox_list_from)
    to_city_extra_doortdoor = dtd_distance(checkbox_list_to)


    # Final result - SCREEN
    ''
    ''
    st.write("##### Calculated values:")
    '' 
    st.write(f"- The distance costs: **{price:,.2f} {selected_currency}**.")
    st.write(f"- The distance: **{distance:,.2f} km**.")
    st.write(f"- Time to cover the distance: **{time_journey:.2f} hour(s)**.")

    if selected_transport == 'Truck':
        st.write(f"- **{selected_transport}** needs this extra time (adminitsration, load etc.):  **{extra_time:.2f} hours(s)** for selected **{urgency}** service - **the SLA** ." )
        st.write(f"- If the distance is longer, there is a need of breaks for driver: **{time_break} hours**.")
        st.write(f"- The **overall time needed** to get to the 'To' city ({to_city}) is **{(time_journey + time_break + extra_time):.2f} hour(s)**." )

    elif selected_transport == 'Train' or 'Airplane':
        st.write(f"- **{selected_transport}** needs this extra time (adminitsration, load etc.):  **{extra_time:.2f} hours(s)** for selected **{urgency}** service - **the SLA** ." )
        st.write(f"- The **overall time needed** to get to the 'To' city ({to_city}) is **{(time_journey + extra_time):.2f} hour(s)**." )
    
    ''
    
    st.write("###### Additional services:")
    st.write(f"- Insurance extra costs: **{money_insurance:,.2f} {selected_currency}**.")
    st.write(f"- Fregile goods costs: **{money_fragile:,.2f} {selected_currency}**.")
    st.write(f"- Danger goods costs: **{money_danger:,.2f} {selected_currency}**.")
    st.write(f"- Door-To-Door - 'From' city ({from_city}):  **{door_from_result:,.2f} {selected_currency}** - ({from_city_extra_doortdoor} km).")
    st.write(f"- Door-To-Door - 'To' city ({to_city}):  **{door_to_result:,.2f} {selected_currency}** - ({to_city_extra_doortdoor} km).")
    
    ''
    st.write("###### Final price:")
    with st.container(border=True):
        st.write(f"**{(price + money_insurance + money_fragile + money_danger + door_to_result + door_from_result):,.2f} {selected_currency}**")
        # st.write(f"**Final price: {(price + money_insurance + money_fragile + money_danger + door_to_result + door_from_result):,.2f} {selected_currency}**.")




    