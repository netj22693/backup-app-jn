import streamlit as st
import pandas as pd
import math
import datetime
import requests
import json
import plotly.express as px
import plotly.graph_objects as go



tranport_types_list = ['Truck','Train','Airplane']


# Price per 1t/per approx 30km (one square on map)

#STANDAR - DELIVERY SERVICE
truck_kc = 1_500
train_kc = 1_200
plane_kc = 15_000

truck_eur = 60
train_eur = 48
plane_eur = 600

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
    "Prague" : {"big" : ["4","10"], "small" : ["10","29"], "train":"y", "air":"y"},
    "Brno" : {"big" : ["5","12"], "small" : ["14","35"], "train":"y", "air":"y"},
    "Olomouc" : {"big" : ["4","13"], "small" : ["12","37"], "train":"n", "air":"n"},
    "Plzen" : {"big" : ["4","9"], "small" : ["12","26"], "train":"n", "air":"n"},
    "Tabor" : {"big" : ["5","10"], "small" : ["13","30"], "train":"n", "air":"n"},
    "Ostrava" : {"big" : ["4","13"], "small" : ["11","39"], "train":"y", "air":"n"},
    "Liberec" : {"big" : ["3","11"], "small" : ["7","31"], "train":"n", "air":"n"},
    "Hradec Kralove" : {"big" : ["4","11"], "small" : ["10","33"], "train":"n", "air":"n"},
    "Pardubice" : {"big" : ["4","11"], "small" : ["10","33"], "train":"y", "air":"y"},
    "Zlin" : {"big" : ["5","13"], "small" : ["14","38"], "train":"n", "air":"n"},
    "Chomutov" : {"big" : ["3","9"], "small" : ["9","26"], "train":"n", "air":"n"},
    "Ceske Budejovice" : {"big" : ["5","10"], "small" : ["15","29"], "train":"n", "air":"n"},
    "Teplice" : {"big" : ["3","9"], "small" : ["8","27"], "train":"n", "air":"n"},
    "Most" : {"big" : ["3","9"], "small" : ["8","27"], "train":"y", "air":"n"},
    "Karlovy Vary" : {"big" : ["3","9"], "small" : ["9","25"], "train":"n", "air":"n"},
    "Kolin" : {"big" : ["4","11"], "small" : ["10","31"], "train":"y", "air":"n"},
    "Ceska Trebova" : {"big" : ["4","12"], "small" : ["11","34"], "train":"y", "air":"n"},
    "Jihlava" : {"big" : ["5","11"], "small" : ["13","31"], "train":"n", "air":"n"},
    "Pisek" : {"big" : ["5","10"], "small" : ["13","28"], "train":"y", "air":"n"},
    # "TEST1" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"n"},
    # "TEST2" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"n"},
    # "TEST3" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"y"},
    # "TEST4" : {"big" : ["3","2"], "small" : ["9","7"], "train":"y", "air":"n"},
},
"sk" : {
	"Bratislava" : {"big" : ["6","12"], "small" : ["18","36"], "train":"y", "air":"y"},
    "Kosice" : {"big" : ["6","16"], "small" : ["16","47"], "train":"y", "air":"y"},
    "Banska Bystrica" : {"big" : ["6","14"], "small" : ["16","40"], "train":"n", "air":"n"}, # tady jsem skoncil
    "Zilina" : {"big" : ["3","7"], "small" : ["14","40"], "train":"y", "air":"n"},	
    "Presov" : {"big" : ["5","16"], "small" : ["15","47"], "train":"n", "air":"n"},	
    "Trnava" : {"big" : ["6","13"], "small" : ["17","39"], "train":"y", "air":"n"},	
    "Trencin" : {"big" : ["5","13"], "small" : ["15","39"], "train":"n", "air":"n"},	
    "Poprad" : {"big" : ["5","15"], "small" : ["14","44"], "train":"y", "air":"n"},	
    "Banska Stiavnica" : {"big" : ["6","14"], "small" : ["17","41"], "train":"n", "air":"n"},
    # "TEST_S1" : {"big" : ["5","7"], "small" : ["13","20"], "train":"n", "air":"n"},	
    # "TEST_S2" : {"big" : ["5","7"], "small" : ["13","20"], "train":"y", "air":"n"},	
    # "TEST_S3" : {"big" : ["5","7"], "small" : ["13","20"], "train":"y", "air":"n"},	
    # "TEST_S4" : {"big" : ["5","7"], "small" : ["13","20"], "train":"y", "air":"y"},	
    # "TEST_S5" : {"big" : ["5","7"], "small" : ["13","20"], "train":"n", "air":"y"},		
},
"at" : {
    "Vienna" : {"big" : ["6","12"], "small" : ["18","34"], "train":"y", "air":"y"},	
    "Innsbruck" : {"big" : ["8","7"], "small" : ["22","21"], "train":"y", "air":"n"},	
    "Linz" : {"big" : ["5","10"], "small" : ["18","28"], "train":"y", "air":"y"},	
    "Salzburg" : {"big" : ["7","9"], "small" : ["20","25"], "train":"y", "air":"y"},	
    "Graz" : {"big" : ["8","11"], "small" : ["22","32"], "train":"y", "air":"y"},	
    "Klagenfurt" : {"big" : ["8","10"], "small" : ["24","29"], "train":"y", "air":"n"},	
    "Villach" : {"big" : ["8","9"], "small" : ["24","27"], "train":"y", "air":"n"},		
},
"de" : {
    "Munich" : {"big" : ["5","7"], "small" : ["18","21"], "train":"y", "air":"y"},	
    "Sonthofen" : {"big" : ["7","6"], "small" : ["17","19"], "train":"y", "air":"n"},	
    "Nuremberg" : {"big" : ["5","7"], "small" : ["13","20"], "train":"y", "air":"y"},	
    "Dresden" : {"big" : ["2","9"], "small" : ["6","27"], "train":"y", "air":"y"},	
    "Chemnitz" : {"big" : ["3","9"], "small" : ["7","25"], "train":"n", "air":"n"},	
    "Bamberg" : {"big" : ["4","7"], "small" : ["11","19"], "train":"y", "air":"n"},	
    "Augsburg" : {"big" : ["6","7"], "small" : ["17","19"], "train":"y", "air":"n"},
    "Würzburg" : {"big" : ["4","5"], "small" : ["11","17"], "train":"y", "air":"n"},		
},
"pl" : {
    "Krakow" : {"big" : ["4","15"], "small" : ["10","43"], "train":"y", "air":"y"},	
    "Novy Sacz" : {"big" : ["4","15"], "small" : ["12","45"], "train":"n", "air":"n"},	
    "Czestochowa" : {"big" : ["3","14"], "small" : ["7","41"], "train":"y", "air":"n"},	
    "Bielsko-Biala" : {"big" : ["4","14"], "small" : ["11","41"], "train":"n", "air":"n"},	
    "Wroclav" : {"big" : ["2","12"], "small" : ["6","36"], "train":"y", "air":"y"},	
    "Katowice" : {"big" : ["3","14"], "small" : ["9","41"], "train":"y", "air":"y"},	
    "Walbrzych" : {"big" : ["3","12"], "small" : ["7","34"], "train":"n", "air":"n"},	
    "Opole" : {"big" : ["3","13"], "small" : ["8","38"], "train":"y", "air":"n"},	
    "Rzeszow" : {"big" : ["4","17"], "small" : ["10","49"], "train":"y", "air":"y"},		
}
})

# //////////////////// API ///////////////////////

def api_get_rate():
    try:
        api_freecurrency_api = "https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_wD1NduThhBnySFJAlV9f6xnQmMhkJa6qFzX7DJz4&currencies=EUR%2CCZK"

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

        usd_to_czk_rate = 21.94
        usd_to_eur_rate = 0.86
        
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

def train_yes(country):

    list_result = []
    for item in dataset_test[country]:
        l2 = dataset_test[country][item]
        l3 = dataset_test[country][item]['train']
        if l3 == 'y':
            list_result.append(item)
    
    return list_result
        

train_at = train_yes('at')
train_de = train_yes('de')
train_pl = train_yes('pl')


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



def train_yes_no(country):

    list_result = []
    for item in dataset_test[country]:
        l3 = dataset_test[country][item]['train']
        list_result.append(l3)
    
    return list_result
        

train_at_yn = train_yes_no('at')
train_de_yn = train_yes_no('de')
train_pl_yn = train_yes_no('pl')


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



def air_yes(country):

    list_result = []
    for item in dataset_test[country]:
        l3 = dataset_test[country][item]['air']
        if l3 == 'y':
            list_result.append(item)
    
    return list_result

air_at = air_yes('at')
air_de = air_yes('de')
air_pl = air_yes('pl')



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


def air_yes_no(country):

    list_result = []
    for item in dataset_test[country]:
        l3 = dataset_test[country][item]['air']
        list_result.append(l3)
    
    return list_result


air_at_yn = air_yes_no('at')
air_de_yn = air_yes_no('de')
air_pl_yn = air_yes_no('pl')




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
train_at_yn_text = text_output(train_at_yn)
train_de_yn_text = text_output(train_de_yn)
train_pl_yn_text = text_output(train_pl_yn)

air_cz_yn_text = text_output(air_cz_yn)
air_sk_yn_text = text_output(air_sk_yn)
air_at_yn_text = text_output(air_at_yn)
air_de_yn_text = text_output(air_de_yn)
air_pl_yn_text = text_output(air_pl_yn)




# Names of cities 
list_cz_az = []
list_cz = []
for item in dataset_test['cz']:
    list_cz.append(item)
    list_cz_az.append(item)



list_sk_az = []
list_sk = []
for item in dataset_test['sk']:
    list_sk.append(item)
    list_sk_az.append(item)


def list_city_az(country):

    list_country_az = []
    list_country = []
    for item in dataset_test[country]:
        list_country.append(item)
        list_country_az.append(item)
    
    list_country_az.sort()

    return list_country_az, list_country

list_at_az, list_at = list_city_az('at')
list_de_az, list_de = list_city_az('de')
list_pl_az, list_pl = list_city_az('pl')


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



table_overview_full_at = pd.DataFrame({
    "City" : list_at,
    "Road" : 'Available',
    "Train" : train_at_yn_text,
    "Airplane" : air_at_yn_text
})

table_overview_full_at.index +=1


table_overview_full_de = pd.DataFrame({
    "City" : list_de,
    "Road" : 'Available',
    "Train" : train_de_yn_text,
    "Airplane" : air_de_yn_text
})

table_overview_full_de.index +=1


table_overview_full_pl = pd.DataFrame({
    "City" : list_pl,
    "Road" : 'Available',
    "Train" : train_pl_yn_text,
    "Airplane" : air_pl_yn_text
})

table_overview_full_pl.index +=1

# Dataset/variables for statistics
count_list_cz = len(list_cz)
count_list_sk = len(list_sk)
count_list_at = len(list_at)
count_list_de = len(list_de)
count_list_pl = len(list_pl)

count_train_cz = len(train_cz)
count_train_sk = len(train_sk)
count_train_at = len(train_at)
count_train_de = len(train_de)
count_train_pl = len(train_pl)

count_air_cz = len(air_cz)
count_air_sk = len(air_sk)
count_air_at = len(air_at)
count_air_de = len(air_de)
count_air_pl = len(air_pl)


count_truck_cz = count_list_cz
count_truck_sk = count_list_sk
count_truck_at = count_list_at
count_truck_de = count_list_de
count_truck_pl = count_list_pl


diff_truck_cz = count_list_cz - count_truck_cz
diff_train_cz = count_list_cz - count_train_cz
diff_air_cz = count_list_cz - count_air_cz

diff_truck_sk = count_list_sk - count_truck_sk
diff_train_sk = count_list_sk - count_train_sk
diff_air_sk = count_list_sk - count_air_sk

diff_truck_at = count_list_at - count_truck_at
diff_train_at = count_list_at - count_train_at
diff_air_at = count_list_at - count_air_at

diff_truck_de = count_list_de - count_truck_de
diff_train_de = count_list_de - count_train_de
diff_air_de = count_list_de - count_air_de

diff_truck_pl = count_list_pl - count_truck_pl
diff_train_pl = count_list_pl - count_train_pl
diff_air_pl = count_list_pl - count_air_pl


data_pie_truck_cz = pd.DataFrame({
                "Number" : [count_truck_cz , diff_truck_cz],
                "Result" : ["Available", "Not available",]
                })

data_pie_train_cz = pd.DataFrame({
                "Number" : [count_train_cz , diff_train_cz],
                "Result" : ["Available", "Not available",]
                })


data_pie_air_cz = pd.DataFrame({
                "Number" : [count_air_cz , diff_air_cz],
                "Result" : ["Available", "Not available",]
                })


data_pie_truck_sk = pd.DataFrame({
                "Number" : [count_truck_sk , diff_truck_sk],
                "Result" : ["Available", "Not available",]
                })

data_pie_train_sk = pd.DataFrame({
                "Number" : [count_train_sk , diff_train_sk],
                "Result" : ["Available", "Not available",]
                })


data_pie_air_sk = pd.DataFrame({
                "Number" : [count_air_sk , diff_air_sk],
                "Result" : ["Available", "Not available",]
                })



data_pie_truck_at = pd.DataFrame({
                "Number" : [count_truck_at , diff_truck_at],
                "Result" : ["Available", "Not available",]
                })

data_pie_train_at = pd.DataFrame({
                "Number" : [count_train_at , diff_train_at],
                "Result" : ["Available", "Not available",]
                })


data_pie_air_at = pd.DataFrame({
                "Number" : [count_air_at , diff_air_at],
                "Result" : ["Available", "Not available",]
                })



data_pie_truck_de = pd.DataFrame({
                "Number" : [count_truck_de , diff_truck_de],
                "Result" : ["Available", "Not available",]
                })

data_pie_train_de = pd.DataFrame({
                "Number" : [count_train_de , diff_train_de],
                "Result" : ["Available", "Not available",]
                })


data_pie_air_de = pd.DataFrame({
                "Number" : [count_air_de , diff_air_de],
                "Result" : ["Available", "Not available",]
                })


data_pie_truck_pl = pd.DataFrame({
                "Number" : [count_truck_pl , diff_truck_pl],
                "Result" : ["Available", "Not available",]
                })

data_pie_train_pl = pd.DataFrame({
                "Number" : [count_train_pl , diff_train_pl],
                "Result" : ["Available", "Not available",]
                })


data_pie_air_pl = pd.DataFrame({
                "Number" : [count_air_pl , diff_air_pl],
                "Result" : ["Available", "Not available",]
                })






data_pie_truck_overall = pd.DataFrame({
                "Number" : [
                    (count_truck_cz + count_truck_sk + count_truck_at + count_truck_de + count_truck_pl),
                    (diff_truck_cz + diff_truck_sk + diff_truck_at + diff_truck_de + diff_truck_pl )],
                "Result" : ["Available", "Not available",]
                })

data_pie_train_overall = pd.DataFrame({
                "Number" : [
                    (count_train_cz + count_train_sk + count_train_at + count_train_de + count_train_pl),
                    (diff_train_cz + diff_train_sk + diff_train_at + diff_train_de + diff_train_pl)],
                "Result" : ["Available", "Not available",]
                })


data_pie_air_overall = pd.DataFrame({
                "Number" : [
                    (count_air_cz + count_air_sk + count_air_at + count_air_de + count_air_pl),
                    (diff_air_cz + diff_air_sk + diff_air_at + diff_air_de + diff_air_pl)],
                "Result" : ["Available", "Not available",]
                })


# //////////////////// Frontend screen - top part ////////////////////////

st.write("# Transport calculation")

''
''
''
''

st.image("Pictures/Function_7/F7_map_V2_v4.svg")
''
''
with st.expander("Delivery area - Central Europe", icon = ":material/pin_drop:"):

    st.image("Pictures/Function_7/F7_map_central_europe.svg")
    pass



with st.expander("City overview", icon = ":material/pin_drop:"):

    ''
    tab_co1, tab_co2, tab_co3, tab_co4, tab_co5 = st.tabs([
        "CZ",
        "SK",
        "AT",
        "DE",
        "PL"
    ])

    with tab_co1:
        st.write("- **Czech Republic:**")
        ''
        st.image("Pictures/Function_7/F7_cities_cz.svg")
        ''
        st.dataframe(table_overview_full_cz)
    
    with tab_co2:
        st.write("- **Slovakia:**")
        ''
        st.image("Pictures/Function_7/F7_cities_sk.svg", width= 520)
        ''        
        st.dataframe(table_overview_full_sk)

    with tab_co3:
        st.write("- **Austria:**")
        ''
        st.image("Pictures/Function_7/F7_cities_at.svg", width= 520)
        ''
        st.dataframe(table_overview_full_at)

    with tab_co4:
        st.write("- **Germany:**")
        ''
        st.image("Pictures/Function_7/F7_cities_de.svg", width= 420)
        ''
        st.dataframe(table_overview_full_de)

    with tab_co5:
        st.write("- **Poland:**")
        ''
        st.image("Pictures/Function_7/F7_cities_pl.svg", width= 420)
        ''
        st.dataframe(table_overview_full_pl)



with st.expander("City statistics - Dashboard", icon = ":material/analytics:"):

    st.write(f"""
             - Number of cities: **{count_list_cz + count_list_sk + count_list_at + count_list_de + count_list_pl}**
                - **CZ** - Czech Republic: **{count_list_cz}**
                - **SK** - Slovakia: **{count_list_sk}**
                - **AT** - Austria: **{count_list_at}**
                - **DE** - Germany: **{count_list_de}**
                - **PL** - Poland: **{count_list_pl}**
             """)
    
    ''
    st.write("Charts show figures/ratio of **how many cities is available** (:green[**GREEN**]) or not available **based on Transport type**.")
    ''

    def pie_chart(df, title_input):
        
        fig_pie = px.pie(
            df, 
            names = "Result",
            values = "Number",
            title = title_input,
            color = "Result",
            color_discrete_map={'Available':'rgba(0, 105, 0, 0.8','Not available':'rgba(175, 175, 175, 0.66)',}
            )
        
        fig_pie.update_traces(texttemplate="%{percent:.2%}")
        fig_pie.update_layout(showlegend = False)

        return fig_pie

    fig_pie_truck_cz = pie_chart(data_pie_truck_cz, "CZ Truck")
    fig_pie_train_cz = pie_chart(data_pie_train_cz, "CZ Train")
    fig_pie_air_cz = pie_chart(data_pie_air_cz, "CZ Airplane")

    fig_pie_truck_sk = pie_chart(data_pie_truck_sk, "SK Truck")
    fig_pie_train_sk = pie_chart(data_pie_train_sk, "SK Train")
    fig_pie_air_sk = pie_chart(data_pie_air_sk, "SK Airplane")

    fig_pie_truck_at = pie_chart(data_pie_truck_at, "AT Truck")
    fig_pie_train_at = pie_chart(data_pie_train_at, "AT Train")
    fig_pie_air_at = pie_chart(data_pie_air_at, "AT Airplane")

    fig_pie_truck_de = pie_chart(data_pie_truck_de, "DE Truck")
    fig_pie_train_de = pie_chart(data_pie_train_de, "DE Train")
    fig_pie_air_de = pie_chart(data_pie_air_de, "DE Airplane")

    fig_pie_truck_pl = pie_chart(data_pie_truck_pl, "PL Truck")
    fig_pie_train_pl = pie_chart(data_pie_train_pl, "PL Train")
    fig_pie_air_pl = pie_chart(data_pie_air_pl, "PL Airplane")

    fig_pie_truck_overall = pie_chart(data_pie_truck_overall, "Truck")
    fig_pie_train_overall = pie_chart(data_pie_train_overall, "Train")
    fig_pie_air_overall = pie_chart(data_pie_air_overall, "Airplane")




    # https://plotly.streamlit.app/Bar_Charts

    # -----  Chart ---- CZ and SK ---- 
    x_cz_sk = [
        ["CZ", "CZ", "CZ", "SK", "SK", "SK", "AT", "AT", "AT", "DE", "DE", "DE", "PL", "PL", "PL"],
        ['Truck','Train', 'Air', 'Truck','Train', 'Air', 'Truck','Train', 'Air', 'Truck','Train', 'Air', 'Truck','Train', 'Air']
    ]

    y_available = [count_truck_cz,count_train_cz,count_air_cz,count_truck_sk,count_train_sk,count_air_sk, count_truck_at,count_train_at,count_air_at, count_truck_de,count_train_de,count_air_de, count_truck_pl,count_train_pl,count_air_pl ]
    y_not_available = [diff_truck_cz,diff_train_cz,diff_air_cz,diff_truck_sk,diff_train_sk,diff_air_sk, diff_truck_at,diff_train_at,diff_air_at, diff_truck_de,diff_train_de,diff_air_de, diff_truck_pl,diff_train_pl,diff_air_pl]


    fig_cz_sk = go.Figure()
    fig_cz_sk.add_bar(x=x_cz_sk,y=y_available, name= "Available", text = y_available,
        marker=dict(
            color='rgba(0, 105, 0, 0.8)',
            # line=dict(color='rgba(7, 7, 7, 1)', width=1)
        )
    )
    
    fig_cz_sk.add_bar(x=x_cz_sk,y=y_not_available, name= "Not available", text = y_not_available,
        marker=dict(
            color='rgba(175, 175, 175, 0.66)',
            # line=dict(color='rgba(7, 7, 7, 1)', width=1)
        )
    )

    fig_cz_sk.update_layout(barmode="relative")
    fig_cz_sk.update_layout(title = "Transport type availability - CZ & SK split")


    # -----  Chart ----  Overall ---- 
    x_overall = ['Truck','Train', 'Airplane']

    y_available_overall = [(count_truck_cz + count_truck_sk + count_truck_at + count_truck_de + count_truck_pl), (count_train_cz + count_train_sk + count_train_at + count_train_de + count_train_pl),(count_air_cz + count_air_sk + count_air_at + count_air_de + count_air_pl)]
    y_not_availab_overall = [(diff_truck_cz + diff_truck_sk + diff_truck_at + diff_truck_de + diff_truck_pl),(diff_train_cz + diff_train_sk + diff_train_at + diff_train_de + diff_train_pl), (diff_air_cz + diff_air_sk + diff_air_at + diff_air_de + diff_air_pl)]

    fig_overall = go.Figure()
    fig_overall.add_bar(x=x_overall,y=y_available_overall, name= "Available", text = y_available_overall,
        marker=dict(
            color='rgba(0, 105, 0, 0.8)',
            # line=dict(color='rgba(7, 7, 7, 1)', width=1)
        )
    )
    fig_overall.add_bar(x=x_overall,y=y_not_availab_overall, name= "Not available", text = y_not_availab_overall,
        marker=dict(
            color='rgba(175, 175, 175, 0.66)',
            # line=dict(color='rgba(7, 7, 7, 1)', width=1)
        )
    )

    fig_overall.update_layout(barmode="relative")
    fig_overall.update_layout(title = "Transport type availability")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "Bar - Split",
        "Bar - Overall",
        "% Overall",
        "% CZ",
        "% SK",
        "% AT",
        "% DE",
        "% PL"
        ])

    with tab1:
        with st.container(border=True):
            st.plotly_chart(fig_cz_sk, theme="streamlit")  
             
    with tab2:
        with st.container(border=True):
            st.plotly_chart(fig_overall, theme="streamlit")

    with tab3:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(fig_pie_truck_overall, use_container_width=False, height = 3000)
            col_stat_2.plotly_chart(fig_pie_train_overall, use_container_width=False)
            col_stat_3.plotly_chart(fig_pie_air_overall, use_container_width=False)

    # CZ
    with tab4:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(fig_pie_truck_cz, use_container_width=False, height = 3000)
            col_stat_2.plotly_chart(fig_pie_train_cz, use_container_width=False)
            col_stat_3.plotly_chart(fig_pie_air_cz, use_container_width=False)

    # SK
    with tab5:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(fig_pie_truck_sk, use_container_width=False, height = 3000)
            col_stat_2.plotly_chart(fig_pie_train_sk, use_container_width=False)
            col_stat_3.plotly_chart(fig_pie_air_sk, use_container_width=False)

    # AT
    with tab6:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(fig_pie_truck_at, use_container_width=False, height = 3000)
            col_stat_2.plotly_chart(fig_pie_train_at, use_container_width=False)
            col_stat_3.plotly_chart(fig_pie_air_at, use_container_width=False)

    # DE
    with tab7:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(fig_pie_truck_de, use_container_width=False, height = 3000)
            col_stat_2.plotly_chart(fig_pie_train_de, use_container_width=False)
            col_stat_3.plotly_chart(fig_pie_air_de, use_container_width=False)

    # PL
    with tab8:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(fig_pie_truck_pl, use_container_width=False, height = 3000)
            col_stat_2.plotly_chart(fig_pie_train_pl, use_container_width=False)
            col_stat_3.plotly_chart(fig_pie_air_pl, use_container_width=False)



            
with st.expander("Currency and rate - API", icon = ":material/payments:"):

    ''
    ''
    col_r1,col_r2 = st.columns(2)

    col_r1.metric(label="USD to CZK", value= usd_to_czk_rate)

    col_r2.metric(label="USD to EUR", value= usd_to_eur_rate)

    ''
    st.write("- This is a **dynamic part** - API based")
    st.write("- **Exchange rate of the day** influences the costs/price within calculations")


    ''
    tab_c1, tab_c2 = st.tabs([
        "Koruna",
        "Euro"
    ])

    with tab_c1:
        st.write("###### CZ - koruna:")
        st.dataframe(crit_dataset_kc, hide_index=True)
        ''

        st.write("Overview:")
        st.write("""
                - These **1-unit** costs per transport type have been set for **default** rate ( 21 <= x < 22 ) for **Standard** delivery service
                """)
        st.caption("**1 unit is approximatelly ~ 30 km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")

        col_r3,col_r4 = st.columns(2)
        col_r3.dataframe(standard_def_kc_df, hide_index=True, use_container_width=True)

        st.write("""
                - In case that the **rate is in** this range the application calculates with these **default** values
                - In case that the **rate is different** the relevant % increas/decrease is calculated **from the default values**
                """)


    with tab_c2:
        st.write("###### SK, AT, DE, PL - euro:")
        st.dataframe(crit_dataset_eur, hide_index=True)
        ''

        st.write("Overview:")
        st.write("""
                - These **1-unit** costs per transport type have been set for **default** rate ( 0.82 <= x < 0.87 ) for **Standard** delivery service
                """)
        st.caption("**1 unit is approximatelly ~ 30 km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")


        col_r3,col_r4 = st.columns(2)
        col_r3.dataframe(standard_def_eur_df, hide_index=True, use_container_width=True)

        st.write("""
                - In case that the **rate is in** this range the application calculates with these **default** values
                - In case that the **rate is different** the relevant % increas/decrease is calculated **from the default values**
                """)

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






# Filters 
''
''
''


col1,col2 = st.columns(2, gap="large")


radio_from_country = col1.radio(
    "Country from:",
    options=["AT","CZ","DE","PL","SK"],
)

radio_from_country = radio_from_country.lower()

if radio_from_country == "cz":
    
    from_city = col1.selectbox("City from:", list_cz_az)
    country_code_from = "CZ"

if radio_from_country == "sk":

    from_city = col1.selectbox("City from:", list_sk_az)
    country_code_from = "SK"

if radio_from_country == "at":
    
    from_city = col1.selectbox("City from:", list_at_az)
    country_code_from = "AT"

if radio_from_country == "de":

    from_city = col1.selectbox("City from:", list_de_az)
    country_code_from = "DE"

if radio_from_country == "pl":

    from_city = col1.selectbox("City from:", list_pl_az)
    country_code_from = "PL"



radio_to_country = col2.radio(
    "Country to:",
    options=["AT","CZ","DE","PL","SK"]
)

radio_to_country = radio_to_country.lower()

if radio_to_country == "cz":
    
    to_city = col2.selectbox("City to:", list_cz_az)
    country_code_to = "CZ"

if radio_to_country == "sk":

    to_city = col2.selectbox("City to:", list_sk_az)
    country_code_to = "SK"

if radio_to_country == "at":
    
    to_city = col2.selectbox("City to:", list_at_az)
    country_code_to = "AT"

if radio_to_country == "de":

    to_city = col2.selectbox("City to:", list_de_az)
    country_code_to = "DE"

if radio_to_country == "pl":

    to_city = col2.selectbox("City to:", list_pl_az)
    country_code_to = "PL"


# function for offering relevant currency to choose from in case that international transport CZ <-> SK

def number_determination(country):
    
    if country == 'at' or country == 'de' or country == 'pl' or country == 'sk':
        num = 0
    
    if country == 'cz':
        num = 1

    return num
    

def offer_currency(radio_from_country,radio_to_country):


    # if radio_from_country == 'sk' and radio_to_country == 'sk':
    #     currency = 'euro'
    #     return currency
    
    # elif radio_from_country == 'cz' and radio_to_country == 'cz':
    #     currency = 'koruna'
    #     return currency
    
    # else:
    #     currency = ['koruna', 'euro']
    #     return currency
    
    num_from = number_determination(radio_from_country)
    num_to = number_determination(radio_to_country)

    result = num_from + num_to

    if result == 0:
        currency = 'euro'
        return currency
    
    if result == 1:
        currency = ['koruna', 'euro']
        return currency
    
    if result == 2:
        currency = 'koruna'
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
    st.write("""- Average speed: **70 km/h**""")
    st.write("""- Every city is available -> no restrictions""")
    st.write("""- But the **driver needs mandatory breaks** which can prolong the journey/delivery time""")


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
               * Example of journey between 9 - 10 hours -> the exception: Most (CZ) - Poprad (SK)
               * Example of journey longer than 9 or 10 hours with 10 hours sleep break: Teplice (CZ) - Kosice (SK) or Karlovy Vary (CZ) - Kosice (SK)
                """)



with st.expander("Train / Rails", icon=":material/train:"):

    ''
    st.write("""- Average speed: **80 km/h**""")
    st.write("""
    -   Train does **not need breaks** for the driver (in comparison with Truck)
        - The transport planning includes also **change of the drivers**, if it is that long
        - Train jurney is **not** interrupted by mandatory breaks  
    """)

    st.write("""- But is **less flexible** - Only some cities connected by rails""")


    data_table_train_cz = pd.DataFrame({
        "City CZ" : train_cz
        })
    

    data_table_train_sk = pd.DataFrame({
        "City SK" : train_sk
        })

    data_table_train_at = pd.DataFrame({
        "City AT" : train_at
        })

    data_table_train_de = pd.DataFrame({
        "City DE" : train_de
        })

    data_table_train_pl = pd.DataFrame({
        "City PL" : train_pl
        })
    
    data_table_train_cz.index += 1
    data_table_train_sk.index += 1
    data_table_train_at.index += 1
    data_table_train_de.index += 1
    data_table_train_pl.index += 1


    tab_t1, tab_t2, tab_t3, tab_t4, tab_t5 = st.tabs([
        "CZ",
        "SK", 
        "AT",
        "DE",
        "PL"
    ])

    with tab_t1:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_cz.svg", width = 580)
        ''
        st.dataframe(data_table_train_cz)

    with tab_t2:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_sk.svg", width = 460)
        ''
        st.dataframe(data_table_train_sk)

    with tab_t3:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_at.svg", width = 430)
        ''
        st.dataframe(data_table_train_at)

    with tab_t4:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_de.svg", width = 360)
        ''
        st.dataframe(data_table_train_de)

    with tab_t5:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_pl.svg", width = 410)
        ''
        st.dataframe(data_table_train_pl)




with st.expander("Airplane", icon=":material/travel:"):
    ''
    st.write("""- Average speed: **700 km/h**""")
    st.write("""- Very expensive but fast -> Benficial for time critical goods/transports""")
    st.write("""- Only some cities connected""")
    ''

    data_table_air_cz = pd.DataFrame({
        "City CZ" : air_cz
        })
    

    data_table_air_sk = pd.DataFrame({
        "City SK" : air_sk
        })

    data_table_air_at = pd.DataFrame({
        "City AT" : air_at
        })
    

    data_table_air_de = pd.DataFrame({
        "City DE" : air_de
        })

    data_table_air_pl = pd.DataFrame({
        "City PL" : air_pl
        })
    

    data_table_air_cz.index += 1
    data_table_air_sk.index += 1
    data_table_air_at.index += 1
    data_table_air_de.index += 1
    data_table_air_pl.index += 1



    tab_a1, tab_a2, tab_a3, tab_a4, tab_a5 = st.tabs([
        "CZ",
        "SK",
        "AT",
        "DE",
        "PL"        
    ])

    with tab_a1:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_cz.svg", width = 580)
        ''
        st.dataframe(data_table_air_cz)

    with tab_a2:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_sk.svg", width = 460)
        ''
        st.dataframe(data_table_air_sk)

    with tab_a3:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_at.svg", width = 430)
        ''
        st.dataframe(data_table_air_at)

    with tab_a4:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_de.svg", width = 360)
        ''
        st.dataframe(data_table_air_de)

    with tab_a5:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_pl.svg", width = 410)
        ''
        st.dataframe(data_table_air_pl)


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



# 19-Aug-2025: This steps calculates price per kilometr (Airplane has a different method of calculation than Truck and Train)
if selected_transport == 'Airplane':
    price_square = price_square / 30





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

if selected_transport == 'Airplane':
    st.write(f" - Unit price for distance calculation: **{(price_square * 30):,.2f}** {selected_currency}")


else:
    st.write(f" - Unit price for distance calculation: **{price_square:,.2f} {selected_currency}**")


# Expanders
''
with st.expander("Unit price", icon= ":material/info:"):

    ''
    st.write("- Is a price per specific distance")
    st.write("- The function/calculation works based on **coordinate system**")
    st.write("- Unit means specific field in this coordinate system")
    st.write("- **Based on the units, distance and price is calculated**")
    st.write("- **1 unit is approximatelly ~ 30 km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")
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


    # Function helping to see number insterted with with split 1_000_000 
    # input comes as int -> change to str -> value as a list -> reverse -> for loop: after every 3rd item add ' '  & 'index != b_len' this prevents to add ' ' space in case that number has 3, 6, 9... numbers. If the condition not there, outcome: ' 100 000', if there '100 000'. -> again reverse of the list -> list back to string -> visualization on user screen
    if shipment_value is not None:

        def formating(shipment_value):
            
            a = str(shipment_value)
            b = list(a)
            b.reverse()
            b_len = len(b)

            index = 0
            list_space = []

            for item in b:
                list_space.append(item)
                index += 1

                if index % 3 == 0 and index != b_len:
                    list_space.append(' ')


            list_space.reverse()
            final_str = ''.join(list_space)
            return final_str


        formated_shipment_value_str = formating(shipment_value)
        st.write(f"- Inserted value: **{formated_shipment_value_str}** {selected_currency}.")

else:
    shipment_value = None


''
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


def radio_button_return_truck(input):

    if input == 'Within city':
        return [True, False, False]

    if input == '10 km':
        return [False, True, False]
    
    if input == '20 km':
        return [False, False, True]
    

def radio_button_return_train_air(input):

    if input == 'No':
        return [True, False, False]

    if input == '10 km':
        return [False, True, False]
    
    if input == '20 km':
        return [False, False, True]




if selected_transport == 'Truck':

    st.write(f"From city ({from_city} - {country_code_from}):")

    radio_dtd_delivery_from_truck = st.radio("radio_from_truck", [
        "Within city",
        "10 km",
        "20 km"
    ],
    index=0,
    horizontal=True,
    label_visibility= "collapsed"
    )
    

    ''
    st.write(f"To city ({to_city} - {country_code_to}):")
  
    radio_dtd_delivery_to_truck = st.radio("radio_to_truck", [
        "Within city",
        "10 km",
        "20 km"
    ],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
    )
    
    checkbox_list_from = radio_button_return_truck(radio_dtd_delivery_from_truck)
    checkbox_list_to = radio_button_return_truck(radio_dtd_delivery_to_truck)
    


if selected_transport == 'Train':


    st.write(f"From city ({from_city} - {country_code_from}):")

    radio_dtd_delivery_from_train = st.radio("radio_from_train", [
        "No",
        "10 km",
        "20 km"
    ],
    index=0,
    horizontal=True,
    key='radio_from_train',
    label_visibility="collapsed"
    )
    

   

    ''
    st.write(f"To city ({to_city} - {country_code_to}):")

    radio_dtd_delivery_to_train = st.radio("radio_to_train", [
        "No",
        "10 km",
        "20 km"
    ],
    index=0,
    horizontal=True,
    key='radio_to_train',
    label_visibility="collapsed"
    )
    
    checkbox_list_from = radio_button_return_train_air(radio_dtd_delivery_from_train)
    checkbox_list_to = radio_button_return_train_air(radio_dtd_delivery_to_train)
    
# Note(!) even if 'Airplane has the same radio button, I use separate 'if' for Train and Air + each has its own radio button with specific 'key' - reason: To have exactly the same behavior of "reseting to index 0 in option, in case that transport type is changed". Radio button is reset to 0 index if: 1) change of transport type
if selected_transport == 'Airplane':

    st.write(f"From city ({from_city} - {country_code_from}):")

    radio_dtd_delivery_from_air = st.radio("radio_from_air", [
        "No",
        "10 km",
        "20 km"
    ],
    index=0,
    horizontal=True,
    key='radio_from_airplane',
    label_visibility="collapsed"
    )
    

    ''
    st.write(f"To city ({to_city} - {country_code_to}):")

    radio_dtd_delivery_to_air = st.radio("radio_to_airplane", [
        "No",
        "10 km",
        "20 km"
    ],
    index=0,
    horizontal=True,
    key='radio_to_airplane',
    label_visibility="collapsed"
    )
    
    checkbox_list_from = radio_button_return_train_air(radio_dtd_delivery_from_air)
    checkbox_list_to = radio_button_return_train_air(radio_dtd_delivery_to_air)

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
        - **Higher price** due to need of **Truck** and **Shipment transfer**
            - **No** - pick up/delivery just from/to Train Station/Airport by Train/Airplane
            - **10 km** radius - **1 000 koruna** ; **40 euro** (Truck needed)
            - **20 km** radius - **1 500 koruna** ; **60 euro** (Truck needed)
    """)


    ''
    st.write("- **More details**:")

    st.link_button(
                label = "Go to Door-to-Door page",
                url="https://dataparsing.streamlit.app/F7_description_dtd",
                help="The button will redirect to the relevant page within this app for download.",
                use_container_width=True,
                icon=":material/launch:"
            )


    ''
    ''
    st.write("###### Simple view/example:")

    st.image("Pictures/Function_7/F7_dtd_legend.svg")

    ''
    st.image("Pictures/Function_7/F7_dtd_abb_air.svg", width= 370)

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
        - Customer pays for delivery to **B - 20km** -> our company will make a shipment transfer from **Airplane to Truck** for the last **20 km**     
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


 
    if (check_isurance or check_fragile or check_danger is True) and shipment_value == None:
        st.warning("You didn't provide Shipment value. Please go up and provide.")
        st.stop()  



    if check_isurance is False  and check_fragile is False and check_danger is False:

        money_insurance = 0
        money_fragile = 0
        money_danger = 0


    # Bug fix 13-Aug-25 - this line prevents case when Truck/Train selected first -> danger goods checked -> change to 'Airplane' so the checked stays (even if the check box is locked) -> app used to calculate the danger value also for Airplane. Fix to make variable always 0
    if selected_transport == 'Airplane':
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



    def calculation_L3B(small_result_r,small_result_c):
        # st.write("LEVEL 3B inside detail calculation - ELSE")
        # st.write(f"LEVEL 3B small result_r: {small_result_r}")
        # st.write(f"LEVEL 3B small result_c: {small_result_c}")


        #long diagonal distance compensation
        comp = small_result_r + small_result_c
        
        km1 = 30

        if comp < 8:
            calcul = (small_result_r + small_result_c - 1)
            
            distance = calcul * 31.57

            price = (distance/km1) * price_square
            # st.write(f"LEVEL 3 if 1 - new price: {price}")

            return price, distance
        
        elif 8 <= comp < 10:
            
            calcul = (small_result_r + small_result_c - 2)

            distance = calcul * 33.08 #musim upravit nemam testovaci vzorky

            price = (distance/km1) * price_square
            # st.write(f"LEVEL 3 if 2 - new price: {price}")

            return price, distance


        elif 10 <= comp < 13:
            calcul = (small_result_r + small_result_c - 2.5)

            distance = calcul * 33.08   #musim upravit nemam testovaci vzorky

            price = (distance/km1) * price_square
            # st.write(f"LEVEL 3 if 3 - new price: {price}")

            return price, distance
        
        elif 13 <= comp < 16:

            pythagoras = math.sqrt(small_result_r ** 2 + small_result_c ** 2)

            distance = 35.68 * pythagoras

            price = (distance/km1) * price_square
            # st.write(f"LEVEL 3 if 4 - new price: {price}")

            return price, distance
        
        # 5 a 6 zkusím pythagorovu větu 
        elif 16 <= comp < 18:

            pythagoras = math.sqrt(small_result_r ** 2 + small_result_c ** 2)

            distance = 34.24 * pythagoras

            price = (distance/km1) * price_square
            # st.write(f"LEVEL 3 if 5 - new price: {price}")

            return price, distance
        

        elif 18 <= comp:

            pythagoras = math.sqrt(small_result_r ** 2 + small_result_c ** 2)
            distance = 36.75 * pythagoras
            price = (distance/km1) * price_square
            # st.write(f"LEVEL 3 if 6- new price: {price}")
            return price, distance



    #Calculation in case that move is on horizontal r=0 or vertical level c=0
    def calculation_L3A_R0C0(small_result_r, small_result_c):

        km1 = 30

        # st.write("LEVEL 3A_R0C0 inside detail calculation")
        # st.write(f"LEVEL 3A_R0C0 small_result_r: {small_result_r}")
        # st.write(f"LEVEL 3A_R0C0 small_result_c: {small_result_c}")

        if small_result_r == 0:
            distance = small_result_c * 31.86
            price = (distance/km1) * price_square
            return price, distance
        

        if small_result_c == 0:
            distance = small_result_r * 31.86
            price = (distance/km1) * price_square
            return price, distance


    # if different big region 
    def calculation_L2(from_small_r, to_small_r, from_small_c, to_small_c):
        # st.write("LEVEL 2 inside detail calculation")
        small_result_r = abs(from_small_r - to_small_r)
        small_result_c = abs(from_small_c - to_small_c)

        if small_result_r <= 1 and small_result_c <= 1:
            price = price_square
            distance = 2 * 24.15     # bug fix 16-Aug-2024 (this 'distance' variable was missing here / UnboundLocalError: cannot access local variable 'distance' where it is not associated with a value)
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


    def calculation_air_L1(from_small_r, to_small_r,from_small_c, to_small_c):
        # st.write(f"L1 air inside")
        small_r = abs(from_small_r - to_small_r)
        small_c = abs(from_small_c - to_small_c)

        pythagoras = math.sqrt(small_r ** 2 + small_c ** 2)
        distance = pythagoras * 26.996  # 26.996 is average measuring of distance
        price = distance * price_square # note: the price_square is price per kilometr for airplane (was adjusted upper in the code)

        return price, distance


    # 19-Aug: here the split which function(s) for calculation to use based on Truck/Train and Airplane 

    if selected_transport == 'Truck' or selected_transport == 'Train':

        price, distance = calculation_L1(from_big_r, to_big_r, from_big_c, to_big_c,from_small_r, to_small_r,from_small_c, to_small_c)

    if selected_transport == 'Airplane':

        # only small coordinates R1C1 
        price, distance = calculation_air_L1(from_small_r, to_small_r,from_small_c, to_small_c)


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


    def door_to_door_time_truck(list_bool):

        if list_bool[0] == True:
            result = 0
            return result

        if list_bool[1] == True:
            result = 0.42       # 10 km ; 25 min -> approx. 0.42 h
            return result
        
        if list_bool[2] == True:
            result = 0.75       # 20 km ; 45 min -> 0.75 h
            return result


    def door_to_door_time_train_air(list_bool):

        transfer_time = 1       # 1 hour ; Transfer between Train/Air <-> Truck 

        if list_bool[0] == True:
            transfer_time = 0       # no DTD no transfer -> 0
            truck_time = 0          # no DTD no transfer -> 0
            result = 0
            return result, transfer_time, truck_time

        if list_bool[1] == True:
            truck_time = 0.42       # 10 km ; 25 min -> approx. 0.42 h
            result = transfer_time + truck_time
            return result, transfer_time, truck_time
        
        if list_bool[2] == True:
            truck_time = 0.75       # 20 km ; 45 min -> 0.75 h
            result = transfer_time + truck_time
            return result, transfer_time, truck_time
            

    if selected_transport == 'Truck':


        time_dtd_from = door_to_door_time_truck(checkbox_list_from)
        time_dtd_to = door_to_door_time_truck(checkbox_list_to)
        
        
        time_dtd = time_dtd_from + time_dtd_to

        time_journy_incl_dtd = time_journey + time_dtd_from + time_dtd_to

        time_break = calcul_time_break(time_journy_incl_dtd)


    

    if selected_transport == 'Train' or selected_transport == 'Airplane':

        time_dtd_from, transfer_time_from, truck_time_dtd_air_train_from = door_to_door_time_train_air(checkbox_list_from)
        time_dtd_to, transfer_time_to, truck_time_dtd_air_train_to  = door_to_door_time_train_air(checkbox_list_to)


        time_dtd = time_dtd_from + time_dtd_to
    
        time_journy_incl_dtd = time_journey + time_dtd_from + time_dtd_to



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

    if selected_transport == 'Truck':
        st.write(f"""
            - Delivery from **{from_city} ({country_code_from})** to **{to_city} ({country_code_to}):**
                - Costs: **{price:,.2f} {selected_currency}**
                - Distance: **{distance:,.2f} km**
                - Time to cover the distance: **{time_journey:.2f} hour(s)**
                - Transport type: **{selected_transport}**
        """)

        ''
        st.write(f"""
            - **Door-to-Door**:
                - Additional: **{from_city_extra_doortdoor + to_city_extra_doortdoor} km** to the distance
                    - {from_city}: {from_city_extra_doortdoor} km
                    - {to_city}: {to_city_extra_doortdoor} km
                - Time to cover the Door-to-Door: **{time_dtd:.2f} hours(s)**
        """)

        ''
        st.write(f"""
            - **{selected_transport}**:
                - Selected service **{urgency}** requires **{extra_time:.2f} hours** for administration, load, etc. - **the SLA**  
                - If longer distance (including Door-to-Door time), **mandatory breaks** for driver: **{time_break} hour(s)**
        """)

        ''
        st.write("- **Overall time end-to-end delivery:**")

        # (round(time_journey, 2) here rounding allowed, because upper |f"- Time to cover the distance {from_city} - {to_city} is: **{time_journey:.2f} hour(s)**."| there is already rounding rounding as part of visualiztion of :.2f
        overall_time_truck = (round(time_journey, 2) + time_break + extra_time + time_dtd)

        if overall_time_truck >= 2:
            hour_s_text_truck = 'hours'

        else:
            hour_s_text_truck = 'hour'

        with st.container(border=True):
            st.write(f"**{overall_time_truck:.2f} {hour_s_text_truck}**")



    elif selected_transport == 'Train' or 'Airplane':
        st.write(f"""
            - Delivery from **{from_city} ({country_code_from})** to **{to_city} ({country_code_to}):**
                - Costs: **{price:,.2f} {selected_currency}**
                - Distance: **{distance:,.2f} km**
                - Time to cover the distance: **{time_journey:.2f} hour(s)**
                - Transport type: **{selected_transport}**
        """)

        ''
        st.write(f"""
            - **Door-to-Door**:
                - Additional: **{from_city_extra_doortdoor + to_city_extra_doortdoor} km** to the distance for which **Truck is needed**
                    - {from_city}: {from_city_extra_doortdoor} km
                    - {to_city}: {to_city_extra_doortdoor} km
                - Time to cover the Door-to-Door: **{time_dtd:.2f} hours(s)**
                    - Transfer {selected_transport} <-> Truck: {transfer_time_from + transfer_time_to} hour(s)
                    - Time for Truck ride: {truck_time_dtd_air_train_from + truck_time_dtd_air_train_to} hour(s)
        """)

        ''
        st.write(f"""
            - **{selected_transport}**:
                - Selected service **{urgency}** requires **{extra_time:.2f} hours** for administration, load, etc. - **the SLA**  
        """)

        ''
        st.write("- **Overall time end-to-end delivery:**")

        # (round(time_journey, 2) here rounding allowed, because upper |f"- Time to cover the distance {from_city} - {to_city} is: **{time_journey:.2f} hour(s)**."| there is already rounding rounding as part of visualiztion of :.2f
        overall_time_train_air = (round(time_journey,2) + extra_time + time_dtd)

        if overall_time_train_air >= 2:
            hour_s_text_train_air = 'hours'

        else:
            hour_s_text_train_air = 'hour'

        with st.container(border=True):
            st.write(f"**{overall_time_train_air:.2f} {hour_s_text_train_air}**")
    


    ''
    ''
    st.write(f"""
    - **Additional services - costs**:
        - Insurance extra costs: **{money_insurance:,.2f} {selected_currency}**
        - Fregile goods costs: **{money_fragile:,.2f} {selected_currency}**
        - Danger goods costs: **{money_danger:,.2f} {selected_currency}**
        - Door-To-Door - {from_city} ({country_code_from}):  **{door_from_result:,.2f} {selected_currency}** - ({from_city_extra_doortdoor} km)
        - Door-To-Door - {to_city} ({country_code_to}):  **{door_to_result:,.2f} {selected_currency}** - ({to_city_extra_doortdoor} km)
    """)


    ''
    ''
    st.write("- **Final price:**")
    with st.container(border=True):
        st.write(f"**{(price + money_insurance + money_fragile + money_danger + door_to_result + door_from_result):,.2f} {selected_currency}**")


# comment for commit


    