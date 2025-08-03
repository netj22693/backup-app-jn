import streamlit as st
import pandas as pd







# Data set 
dataset_test = ({
"cz" : {
    "A" : {"big" : ["1","1"], "small" : ["2","2"], "train":"y", "air":"y"},
    "B" : {"big" : ["2","1"], "small" : ["5","2"], "train":"n", "air":"y"},
    "C" : {"big" : ["2","2"], "small" : ["5","5"], "train":"n", "air":"n"},
    "D" : {"big" : ["2","3"], "small" : ["5","8"], "train":"n", "air":"n"},
    "E" : {"big" : ["1","1"], "small" : ["2","3"], "train":"n", "air":"n"},
    "G" : {"big" : ["2","1"], "small" : ["6","3"], "train":"n", "air":"n"},
    "H" : {"big" : ["2","2"], "small" : ["6","4"], "train":"y", "air":"y"},
    "I" : {"big" : ["3","1"], "small" : ["9","2"], "train":"y", "air":"y"},
    "K" : {"big" : ["1","3"], "small" : ["2","9"], "train":"n", "air":"y"}
},
"sk" : {
	"SA" : {"big" : ["3","4"], "small" : ["8","11"], "train":"n", "air":"y"},
    "SB" : {"big" : ["4","4"], "small" : ["11","11"], "train":"n", "air":"y"},
    "SC" : {"big" : ["4","5"], "small" : ["11","14"], "train":"n", "air":"n"},
    "SD" : {"big" : ["3","5"], "small" : ["8","13"], "train":"y", "air":"y"}		
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


# Names of cities 
list_cz = []
for item in dataset_test['cz']:
    list_cz.append(item)

# st.write(list_cz)


list_sk = []
for item in dataset_test['sk']:
    list_sk.append(item)


# st.write(list_sk)


# Table overview - data set 

table_overview_full_cz = pd.DataFrame({
    "City" : list_cz,
    "Road" : 'y',
    "Train" : train_cz_yn,
    "Airplane" : air_cz_yn
})

table_overview_full_cz.index +=1


table_overview_full_sk = pd.DataFrame({
    "City" : list_sk,
    "Road" : 'y',
    "Train" : train_sk_yn,
    "Airplane" : air_sk_yn
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
def price_decision(selected_currency):
    if selected_currency == 'koruna':
        price_square = 50
        return price_square
    
    if selected_currency == 'euro':
        price_square = 2.5
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
    
    from_city = col1.selectbox("City from:", list_cz)

if radio_from_country == "sk":

    from_city = col1.selectbox("City from:", list_sk)





radio_to_country = col2.radio(
    "Country to:",
    options=["CZ","SK"]
)

radio_to_country = radio_to_country.lower()

if radio_to_country == "cz":
    
    to_city = col2.selectbox("City to:", list_cz)

if radio_to_country == "sk":

    to_city = col2.selectbox("City to:", list_sk)




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

price_square = price_decision(selected_currency)


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
        train_result = ['Airplaine']
    else:
        train_result = []
        
    return train_result

air_result = options_air_result(air_from, air_to)



transport_options_list = train_result + air_result
''
selected_transport = st.radio("Transport type:", transport_options_list)

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
            price = (small_result_r + small_result_c - 1) * price_square
            return price
        
        elif 8 <= comp < 10:
            price = (small_result_r + small_result_c - 2) * price_square
            st.write(f"LEVEL 3 if 2 - před navratem price: {price}")
            return price


        elif 10 <= comp < 13:
            price = (small_result_r + small_result_c - 3) * price_square
            st.write(f"LEVEL 3 if 3 -před navratem price: {price}")
            return price
        
        elif 13 <= comp < 16:
            price = (small_result_r + small_result_c - 6) * price_square
            st.write(f"LEVEL 3 if 4 -před navratem price: {price}")
            return price
        
        elif 16 <= comp:
            price = (small_result_r + small_result_c - 8) * price_square
            st.write(f"LEVEL 3 if 5 -před navratem price: {price}")
            return price


    #Calculation in case that move is on horizontal r=0 or vertical level c=0
    def calculation_L3A_R0C0(small_result_r, small_result_c):
        st.write("LEVEL 3A_R0C0 inside detail calculation")
        st.write(f"LEVEL 3A_R0C0 small_result_r: {small_result_r}")
        st.write(f"LEVEL 3A_R0C0 small_result_c: {small_result_c}")

        if small_result_r == 0:
            price = small_result_c * price_square
            st.write(f"LEVEL 3B small_result_c price *50: {price}")
            return price
        
        if small_result_c == 0:
            price = small_result_r * price_square
            st.write(f"LEVEL 3B small_result_r price *50: {price}")
            return price


    # if different big region 
    def calculation_L2(from_small_r, to_small_r, from_small_c, to_small_c):
        st.write("LEVEL 2 inside detail calculation")
        small_result_r = abs(from_small_r - to_small_r)
        small_result_c = abs(from_small_c - to_small_c)

        if small_result_r <= 1 and small_result_c <= 1:
            price = price_square
            return price
        
        elif small_result_r == 0 or small_result_c == 0:
            price = calculation_L3A_R0C0(small_result_r, small_result_c)
            return price
        
        else:
            price = calculation_L3B(small_result_r,small_result_c)
            return price



    # if big R = C -> same price
    def calculation_L1(from_big_r,
                            to_big_r,
                            from_big_c,
                            to_big_c,
                            from_small_r,
                            to_small_r,
                            from_small_c,
                            to_small_c):
        
        big_result_r = abs(from_big_r - to_big_r)
        big_result_c = abs(from_big_c - to_big_c)
        st.write(f" LEVEL 1: big_result_r: {big_result_r}")
        st.write(f" LEVEL 1: big_result_c: {big_result_c}")

        if big_result_r == 0 and big_result_c == 0:
            price = price_square
            return price

        else:
            st.write("LEVEL 1: Else happened")
            price = calculation_L2(from_small_r, to_small_r, from_small_c, to_small_c)
            return price




    price = calculation_L1(from_big_r,
                            to_big_r,
                            from_big_c,
                            to_big_c,
                            from_small_r,
                            to_small_r,
                            from_small_c,
                            to_small_c)

    st.write(f"po def returnu price {price}")

    #Fronted 
    st.write(f"- Price is: {price} {selected_currency}")






