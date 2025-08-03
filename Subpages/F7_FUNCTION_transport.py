import streamlit as st
import pandas as pd
import math




# Price per 1t/per approx 30km (one square on map)

truck_kc = 689
train_kc = 230
plane_kc = 4_590


truck_eur = 27
train_eur = 9
plane_eur = 180


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




# function for offering relevant currencz to choose from in case that international transport CZ <-> SK
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
st.write(f"price square after function: {price_square}")

''
with st.expander("Truck / Road", icon=":material/local_shipping:"):

    ''
    st.write("""- Every city is available -> no restrictions""")

with st.expander("Train / Rails", icon=":material/train:"):
    ''
    st.write("""- Only some cities connected""")
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
    st.write("""- Only some cities connected""")
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


# //////////////// Submit button ////////////////////

''
''
''
if st.button("Submit", use_container_width=True):
    st.write(from_city)
    st.write(to_city)



    def input_validation(from_city,to_city):
        if from_city == to_city:
            st.warning("City From and To is the same -> They need to be different")
            st.stop()
        
        else:
            pass

    input_validation(from_city,to_city)


    def pars_from_city(from_city, dataset_test):
        
        st.write(f"ve funkci {radio_from_country}")
        st.write(f"ve funkci {from_city}")
 
        from_big = dataset_test[radio_from_country][from_city]['big']
        st.write(f"ve funkci from big - parsed: {from_big}")

        from_small = dataset_test[radio_from_country][from_city]['small']
        st.write(f"ve funkci from small - parsed: {from_small}")



        return from_big, from_small

        
    def pars_to_city(to_city, dataset_test):
        
        st.write("jsem tu?")
        to_big = dataset_test[radio_to_country][to_city]['big']
        to_small = dataset_test[radio_to_country][to_city]['small']
        st.write("parsed?")
        return to_big, to_small



    from_big, from_small = pars_from_city(from_city, dataset_test)
    st.write(f"FROM: po ukonceni def -> city: {from_city} retrun big: {from_big}, small: {from_small} ")

    to_big, to_small = pars_to_city(to_city, dataset_test)
    st.write(f"TO: po ukonceni def -> city: {to_city} retrun big: {to_big}, small: {to_small} ")


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


    st.write(f"after function from_big R: {from_big_r}, C: {from_big_c}")
    st.write(f"after function from_small R: {from_small_r}, C: {from_small_c}")

    st.write(f"after function to_big R: {to_big_r}, C: {to_big_c}")
    st.write(f"after function to_small R: {to_small_r}, C: {to_small_c}")



    def calculation_L3B(small_result_r,small_result_c):
        st.write("LEVEL 3B inside detail calculation - ELSE")
        st.write(f"LEVEL 3B small result_r: {small_result_r}")
        st.write(f"LEVEL 3B small result_c: {small_result_c}")

        #long diagonal distance compensation
        comp = small_result_r + small_result_c
        st.write(f"LEVEL 3 comp {comp}")


        if comp < 8:
            calcul = (small_result_r + small_result_c - 1)
            price = calcul * price_square
            st.write(f"LEVEL 3 if 1 - před navratem price: {price}")

            distance = calcul * 31.57
            return price, distance
        
        elif 8 <= comp < 10:
            calcul = (small_result_r + small_result_c - 2)
            price = calcul * price_square
            st.write(f"LEVEL 3 if 2 - před navratem price: {price}")

            distance = calcul * 33.08 #musim upravit nemam testovaci vzorky
            return price, distance


        elif 10 <= comp < 13:
            calcul = (small_result_r + small_result_c - 2.5)
            price = calcul * price_square
            st.write(f"LEVEL 3 if 3 -před navratem price: {price}")

            distance = calcul * 33.08   #musim upravit nemam testovaci vzorky
            return price, distance
        
        elif 13 <= comp < 16:
            calcul = (small_result_r + small_result_c - 4)
            price = calcul * price_square
            st.write(f"LEVEL 3 if 4 -před navratem price: {price}")

            distance = calcul * 35.68
            return price, distance
        
        elif 16 <= comp < 18:
            calcul = (small_result_r + small_result_c - 5)
            price = calcul * price_square
            st.write(f"LEVEL 3 if 5 -před navratem price: {price}")

            distance = calcul * 34.24
            return price, distance
        
        elif 18 <= comp:
            calcul = (small_result_r + small_result_c - 8)
            price = calcul * price_square
            st.write(f"LEVEL 3 if 6 -před navratem price: {price}")

            distance = calcul * 36.75
            return price, distance



    #Calculation in case that move is on horizontal r=0 or vertical level c=0
    def calculation_L3A_R0C0(small_result_r, small_result_c):
        st.write("LEVEL 3A_R0C0 inside detail calculation")
        st.write(f"LEVEL 3A_R0C0 small_result_r: {small_result_r}")
        st.write(f"LEVEL 3A_R0C0 small_result_c: {small_result_c}")

        if small_result_r == 0:
            st.write("tady?")
            price = small_result_c * price_square
            st.write(f"LEVEL 3A small_result_c price *50: {price}")
            distance = small_result_c * 31.86
            return price, distance
        
        if small_result_c == 0:
            st.write("nebo tady?")
            st.write(small_result_r)
            st.write(price_square)
            price = small_result_r * price_square
            st.write("co tady")
            st.write(f"LEVEL 3A small_result_r price square: {price_square}")
            st.write(f"LEVEL 3A small_result_r: {small_result_r}")
            st.write(f"LEVEL 3A small_result_r price *50: {price}")
            distance = small_result_r * 31.86
            return price, distance


    # if different big region 
    def calculation_L2(from_small_r, to_small_r, from_small_c, to_small_c):
        st.write("LEVEL 2 inside detail calculation")
        small_result_r = abs(from_small_r - to_small_r)
        small_result_c = abs(from_small_c - to_small_c)

        st.write(f"LEVEL 2: small r : {small_result_r}")
        st.write(f"LEVEL 2: small c : {small_result_c}")

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
        st.write(f" LEVEL 1: big_result_r: {big_result_r}")
        st.write(f" LEVEL 1: big_result_c: {big_result_c}")

        if (big_result_r == 0 and big_result_c == 0) and (small_result_r <= 1 and small_result_c <= 1):
            price = price_square
            distance = 24.15
            return price, distance

        else:
            st.write("LEVEL 1: Else happened")
            price, distance = calculation_L2(from_small_r, to_small_r, from_small_c, to_small_c)
            return price, distance




    price, distance = calculation_L1(from_big_r, to_big_r, from_big_c, to_big_c,from_small_r, to_small_r,from_small_c, to_small_c)

    st.write(f"po def returnu price {price}")
    st.write(f"po def returnu distance {distance}")


    # extra time for load unload and other admin stuff (in hours -> day)
    extra_time_truck_h = 8
    extra_time_train_h = 6
    extra_time_air_h = 10

    log_extra_time_truck = extra_time_truck_h / 24
    log_extra_time_train = extra_time_train_h / 24   
    log_extra_time_airplane = extra_time_air_h / 24  
    st.write(f"log extea time: {log_extra_time_truck}")

    def calcul_delivery_time(distance,selected_transport,log_extra_time_truck,log_extra_time_train, log_extra_time_airplane, extra_time_truck_h, extra_time_train_h, extra_time_air_h):

        if selected_transport == 'Truck':
            time_journey = distance / 70
            time = time_journey + extra_time_truck_h
            extra_time_h = extra_time_truck_h
            extra_time_d = log_extra_time_truck
            return time, extra_time_h, extra_time_d,time_journey 

        if selected_transport == 'Train':
            time_journey = distance / 80
            time = time_journey + extra_time_train_h
            extra_time_h = extra_time_train_h
            extra_time_d = log_extra_time_train
            return time, extra_time_h, extra_time_d,time_journey 
        
        if selected_transport == 'Airplane':
            time_journey = distance / 700, 2
            st.write(time_journey)
            time = time_journey + extra_time_air_h, 2
            extra_time_h = extra_time_air_h
            extra_time_d = log_extra_time_airplane
            return time, extra_time_h, extra_time_d,time_journey 

    calculated_time_delivery, extra_time, extra_time_d, time_journey  = calcul_delivery_time(distance,selected_transport,log_extra_time_truck,log_extra_time_train, log_extra_time_airplane, extra_time_truck_h, extra_time_train_h, extra_time_air_h )




    # CO UDELAT: je potřeba znovu napsat tuhle část appky, kvůli rounding ta čísla pak nevycházejí -> je potřeba postupovat přesně v pořadí v jakém ty hodnoty zobrazuju -> v tm pořadí ty hodnoty i počítat VYKAŠLAT SE NA ROUNDING A ZOBRAZOVAT 2 DESETINNÁ MÍSTA :.2F


    # Final numbers + Rounding before visualizition:

    calculated_time_delivery_d = calculated_time_delivery / 24

    buffer_d = 0.5
    guaranted_delivery_d = calculated_time_delivery_d + buffer_d + extra_time_d

    time_journey_d = (time_journey / 24)

    st.write(time_journey_d)
    st.write(extra_time_d)
    st.write(calculated_time_delivery_d)


    #Frontend 
    st.write(f"- Price is: {price:.2f} {selected_currency}")
    st.write(f"- Approximate distance: {distance:.2f} km")
    st.write(f"- Selected transport type: {selected_transport}")
    st.write(f"- Time to cover the distance: {time_journey:.2f} hours -> {time_journey_d:.2f} day(s).")
    st.write(f"- Selected transport type: {selected_transport} needs {extra_time:.2f} hours for administration /load / unload  -> {extra_time_d:.2f} day.")
    st.write(f"- Expected time for delivery: {calculated_time_delivery:.2f} hours -> {calculated_time_delivery_d:.2f} day(s).")
    ''
    st.write(f"- Overall: Guaranted delivery (including 0.5 day buffer) {guaranted_delivery_d:.2f} day(s).")






