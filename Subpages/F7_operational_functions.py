import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import time
import math
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from plotly.graph_objects import Figure
from pandas.io.formats.style import Styler
from sqlalchemy import Engine, create_engine


# ===== DB connection =====
def db_connection() -> Engine:

    # Load secrets
    password = st.secrets["neon"]["password"]
    endpoint = st.secrets["neon"]["endpoint"]

    # connection string
    try: 
        conn_string = f"postgresql+psycopg2://neondb_owner:{password}@{endpoint}.c-4.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

        engine = create_engine(conn_string)
        return engine

    except:
        st.warning("DB not connected - the function will not function fully.")
        return None

# ===== DB related function =====
def create_offer_number(engine: Engine) -> str:

    query = f"""
    SELECT MAX(offer_id) AS offer_id
    FROM function7.offer
    """

    df_query_result = pd.read_sql(query, engine)

    query_result_str = df_query_result['offer_id'].iloc[0]

    prefix = query_result_str[0:3]
    number = int(query_result_str[3:])
    
    next_number = str(number + 1)

    next_offer_number = str(prefix + next_number)

    return next_offer_number

# ===== API =====
def api_get_rate() -> tuple[float, float]:
    
    try:

        api_key = st.secrets["F7_api"]["password_7"]

        api_freecurrency_api = f"https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&currencies=EUR%2CCZK"

        #get reguest
        @st.cache_data(ttl=3600)
        def get_response_api(api_freecurrency_api):
            api_1 = requests.get(api_freecurrency_api, verify=False, timeout=5).text
            return api_1

        api_1 = get_response_api(api_freecurrency_api)


        # JSON format creation
        api_1_json = json.loads(api_1)


        # Parsing
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

        # MAIN - Testing rate for my documentation is 
        usd_to_czk_rate = 21.94
        usd_to_eur_rate = 0.86

        # Rate used for creation of USE CASES -> for tetsing/validation with my UCs in the documentation
        usd_to_czk_rate = 20.66
        usd_to_eur_rate = 0.85
        
        return usd_to_czk_rate, usd_to_eur_rate 


# ===== Operational functions =====
def create_df_cost_trend(currency: str, a:dict) -> pd.DataFrame:

    '''
    - Cost trend -> visualization
    - Creation of DF for UI purpose
    '''

    df = pd.DataFrame([
        {
            "Rule": x["rule_text"],
        "Impact (%)": x["impact_pct"],
            "Impact": x["cost_trend"]
        }
        for x in a[currency]
    ])

    return df


def create_list_transport(a: dict) -> list:

    list_transport = a.keys()
    list_transport = [x.capitalize() for x in list_transport]

    return list_transport


def create_df_extra_time(a: dict, list_transport: list) -> pd.DataFrame:

    list_slow = []
    list_standard = []
    list_express = []

    for transport, level in a.items():
        slow = level["slow"]["extra_time"]
        list_slow.append(slow)

        standard = level["standard"]["extra_time"]
        list_standard.append(standard)

        express = level["express"]["extra_time"]
        list_express.append(express)


    df = pd.DataFrame({
        "Transport" :list_transport,
        "Express" : list_express,
        "Standard" : list_standard ,
        "Slow" : list_slow
    })

    return df


def create_df_default_costs(a: dict, list_transport: list, currency_key: str, currency_ui: str) -> Styler:

    list_default_costs = []

    for transport, level_currency in a.items():
        price = level_currency[currency_key]["standard"]
        list_default_costs.append(price)

    df = pd.DataFrame({
        "Transport" : list_transport,
        "Default": list_default_costs,
        "Currency": currency_ui
    })


    df_styled = df.style.format({
    "Default": "{:,.2f}"
    })

    return df_styled



def determin_square_price_per_rate(price: dict, criteria: dict, currency: str, transport: str, rate_value: float) -> float:


    rounding = {
        "kc" : 0,
        "eur" : 2
    }

    transport_price = price[transport][currency]["standard"]

    criterium = criteria[currency]
    
    for criterion in criterium:
        min_value = criterion["min"]
        max_value = criterion["max"]

        if (
            (min_value is None or rate_value >= min_value)
            and
            (max_value is None or rate_value < max_value)
        ):
            
            impact_pct = criterion["impact_pct"]

            return round(transport_price + ( transport_price / 100) * impact_pct, rounding.get(currency))

        else:
            pass


def get_list_cities_if_transport_available(a:dict, country_code: str, transport: str) -> tuple[list, list]:

    list_result = []


    for item in a[country_code]:
        l3 = a[country_code][item][transport]
        
        if l3 == 'y':
            list_result.append(item)

    count = len(list_result)
    
    return list_result, count


def adjust_text_for_ui(a: list) -> list:

    output = []
    for i in a:
        if i == 'y':
            output.append('Available')
        elif i == 'n':
            output.append('No')

    return output


def create_df_transport_overview(dataset:dict, country_code: str) -> pd.DataFrame:

    list_city = []
    list_train = []
    list_air = []

    for city in dataset[country_code]:
        train = dataset[country_code][city]["train"]
        air = dataset[country_code][city]["air"]

        list_city.append(city)
        list_train.append(train)
        list_air.append(air)


    df = pd.DataFrame({
    "City" : list_city,
    "Road" : 'Available',
    "Train" : adjust_text_for_ui(list_train),
    "Airplane" : adjust_text_for_ui(list_air)
    })

    # Reset index to have nice order 0, 1, 2... after the sorting
    df = df.sort_values("City").reset_index(drop=True)

    df.index +=1

    return df

def create_df_particular_transport_overview(data_input: list, column_name: str) -> pd.DataFrame:

        df = pd.DataFrame({
        column_name : data_input
        })

        # Reset index to have nice order 0, 1, 2... after the sorting
        df = df.sort_values(column_name).reset_index(drop=True)

        df.index +=1

        return df


def get_list_cities(a: dict, country_code: str) -> tuple[list, int]:

    # list_country_az = []
    list_country = []

    for item in a[country_code]:
        list_country.append(item)
        # list_country_az.append(item)
    
    list_country.sort()
    count = len(list_country)

    return list_country, count


def get_currency_option(country_code_from: str, country_code_to: str) -> list:

    '''
    Function to provide currency to offer on UI based on selected countries
    Dict mapping currency to country code
    Currency priority is for sorting of the list    
    '''

    country = {
        "euro": {
            "country": ["at", "de", "pl", "sk"],
            "currency_priority": 2
        },
        "koruna": {
            "country": ["cz"],
            "currency_priority": 1
        }
    }

    list_currency = []

    for currency_name, currency_data in country.items():

        countries = currency_data["country"]


        if (
            country_code_from in countries
            or country_code_to in countries
        ):
            list_currency.append(currency_name)


    return sorted(list_currency, key=lambda x: country[x]["currency_priority"])
            

def get_list_available_transport_based_on_selected_cities(dataset: dict, country_code_from: str, country_code_to: str, from_city: str, to_city: str):

    air_from = dataset[country_code_from][from_city]['air']
    air_to = dataset[country_code_to][to_city]['air']

    train_from = dataset[country_code_from][from_city]['train']
    train_to = dataset[country_code_to][to_city]['train']

    # Truck is default as available in every city
    list_transport = ['Truck']

    if air_from == 'y' and air_to == 'y':
        list_transport.append('Airplane')

    if train_from == 'y' and train_to == 'y':
        list_transport.append('Train')

    priority_list = {
        "Airplane" : 3,
        "Train" : 2,
        "Truck" : 1,

    }

    return sorted(list_transport, key=lambda x: priority_list[x])


def get_price_per_square(dataset:dict, selected_currency: str, selected_transport: str) -> float:

    return dataset[selected_currency][selected_transport]


def get_price_changed_per_service_type(dataset:dict, price_input: float, transport_input: str, selected_service: str) -> float:

    '''
    Calculate new value for price per square in case that selected servise is different than STANDARD
    '''

    # Lowering of transport 'Truck' -> 'truck' (dictionary uses key lower)
    transport_input = transport_input.lower()

    if selected_service == 'Express':

        coef = dataset[transport_input]['express']['coef']
        price = price_input + (price_input * coef)


    elif selected_service == 'Slow':

        coef = dataset[transport_input]['slow']['coef']
        price = price_input - (price_input * coef)

    return price


def get_prices_extra_services(extra_service_dict: dict, shipment_value: int, extra_service: bool, extra_service_text: str):
       
    if extra_service == True:
        return shipment_value / 100 * extra_service_dict[extra_service_text]
    else:
        return 0



def get_extra_time_per_service_sla(dataset:dict, transport_input: str, selected_service: str) -> int:

    '''
    Lookup function to get value 
    '''

    # Lowering of transport 'Truck' -> 'truck' (dictionary uses key lower)
    transport_input = transport_input.lower()
    selected_service = selected_service.lower()

    return dataset[transport_input][selected_service]['extra_time']



def get_coordinates(dataset: dict, country: str, city: str, coordinates_type: str) -> int:
    '''
    To get coordinates saved in the main dictionary based on the input
    '''

    # Parsing to list
    coordinates_list = dataset[country][city][coordinates_type]
    coordinates_list = list(map(int, coordinates_list))

    return coordinates_list[0], coordinates_list[1]

# ===== Distance functions - supporting functions =====

def calculate_pythagoras(a:int, b: int) -> float:
    return math.sqrt(a ** 2 + b ** 2)

# ===== Distance functions =====

def L0_is_in_correction_list(from_city: str, to_city: str, correction_list_data: dict, price_square: float, unit_distance: int) -> tuple[float, float, bool]: 

    '''
    Function checks against 'correction_list_datatset' if selected combination of cities is there or not. If yes -> it takes the defined distance + calculates price
    '''
        
    for item in correction_list_data:

        item1 = item['city1']
        item2 = item['city2']

        if (item1 == from_city and item2 == to_city) or (item1 == to_city and item2 == from_city):

            distance = item['distance']
            price = ((price_square/unit_distance) * distance)
            result = True

            return distance, price, result
    
    return 0, 0, False


def get_calculation_price_distance(coordinates: dict, price_square: float, unit_distance: float) -> tuple[float, float]:
    '''
    Main function for calculating of distance between selected cities and price based on the distance
    There is multiple if/elif/else conditions based on move (within unit/horizontal/vertical/diagonal) on the map 
    It uses coeficitiens accordingly to type of move to get relevant results
    '''
    
    from_coord = coordinates["from"]
    to_coord = coordinates["to"]

    big_result_r = abs(from_coord["big_r"] - to_coord["big_r"])
    big_result_c = abs(from_coord["big_c"] - to_coord["big_c"])
    small_result_r = abs(from_coord["small_r"] - to_coord["small_r"])
    small_result_c = abs(from_coord["small_c"] - to_coord["small_c"])


    # L1
    if (big_result_r == 0 and big_result_c == 0) and (small_result_r <= 1 and small_result_c <= 1):
        print("L1")

        return price_square, unit_distance


    # L2
    elif small_result_r <= 1 and small_result_c <= 1:
        print("L2")

        distance = 2 * 24.15 
        price = price_square

        return price, distance

    # L3A
    elif small_result_r == 0 or small_result_c == 0:

        # L3A_R0C0
        if small_result_r == 0:
            print("L3A_R0C0 - 1")

            distance = small_result_c * 31.86
            price = (distance/unit_distance) * price_square

            return price, distance
        

        elif small_result_c == 0:
            print("L3A_R0C0 - 2")

            distance = small_result_r * 31.86
            price = (distance/unit_distance) * price_square

            return price, distance
        
    # L3B
    else:
        comp = small_result_r + small_result_c
                
        if comp < 8:
            print("L3B - 1")

            distance = 35.5 * calculate_pythagoras(small_result_r, small_result_c)
            price = (distance/unit_distance) * price_square

            return price, distance


        elif 8 <= comp < 10:
            print("L3B - 2")

            calcul = (small_result_r + small_result_c - 2)

            distance = calcul * 33.08 #musim upravit nemam testovaci vzorky

            price = (distance/unit_distance) * price_square

            return price, distance


        elif 10 <= comp < 13:
            print("L3B - 3")
            
            distance = 33.2 * calculate_pythagoras(small_result_r, small_result_c)
            price = (distance/unit_distance) * price_square

            return price, distance
        
        
        elif 13 <= comp < 16:
            print("L3B - 4")

            distance = 35.68 * calculate_pythagoras(small_result_r, small_result_c)
            price = (distance/unit_distance) * price_square

            return price, distance
        
        # 5 a 6 zkusím pythagorovu větu 
        elif 16 <= comp < 18:
            print("L3B - 5")

            distance = 34.24 * calculate_pythagoras(small_result_r, small_result_c)
            price = (distance/unit_distance) * price_square

            return price, distance
        

        elif 18 <= comp:
            print("L3B - 6")

            distance = 36.75 * calculate_pythagoras(small_result_r, small_result_c)
            price = (distance/unit_distance) * price_square

            return price, distance

        else:
            print("ERROR in: get_calculation_price_distance - if/elif/else condition not set")



def get_calculation_price_distance_air(from_small_r: int, to_small_r: int, from_small_c: int,  to_small_c: int, price_square: float) -> tuple[float, float]:
    '''
    Main function for calculating of distance between selected cities and price based on the distance
    AIRPLANE
    uses diagonal move
    '''

    print("L1 - AIR")

    small_r = abs(from_small_r - to_small_r)
    small_c = abs(from_small_c - to_small_c)
   
    #  26.996 is average measuring of distance
    distance = 26.996 * calculate_pythagoras(small_r, small_c)

    # note: price_square is price per kilometer for airplane (was adjusted upper in the code main.py)
    price = distance * price_square

    return price, distance


def get_calculation_delivery_time(distance: float, selected_transport: str, transport_speed: dict) -> float:

    '''
    Function for calculation of how much time is needed specific distance
    Calculation based on speed of selected trynsport type
    '''

    # Lowering: selected_transport 'Truck' but dict works with 'truck'
    selected_transport = selected_transport.lower()

    return distance / transport_speed[selected_transport]



def get_door_to_door_time_truck(dtd_values: dict, selected_dtd: str) -> tuple[float, float, float]:

        return dtd_values[selected_dtd]['truck_driving']


def get_door_to_door_time_train_airplane(dtd_values: dict, selected_dtd: str) -> tuple[float, float, float]:

        if selected_dtd == "No" or selected_dtd == "Within city":
            return  0, 0, 0

        else:
            transfer_time = dtd_values['transfer']
            truck_time = dtd_values[selected_dtd]['truck_driving']
            overall_time = transfer_time + truck_time

            return overall_time, transfer_time, truck_time


def get_door_to_door_cost_and_distance(dtd_values: dict, selected_dtd: str, currency: str, selected_transport: str) -> tuple[float, float]:

    selected_transport = selected_transport.lower()

    dtd_price = dtd_values[selected_dtd]['price'][selected_transport][currency]
    dtd_distance = dtd_values[selected_dtd]['distance']

    return dtd_price, dtd_distance

# ===== Functions change of variable interpretation =====

def format_transport_value(transport_options: list, transport_name: str, value_input: float, round_to: int) -> float | str:

    if transport_name in transport_options:
        return round(value_input, round_to)

    else:
        return 'n/a'


def format_transport_value_using_zero(transport_options: list, transport_name: str, value_input: float, round_to: int) -> float | int:
    '''
    Formatting using '0' if transport not in list
    For CHART purposes -> Chart works with 0
    '''

    if transport_name in transport_options:
        return round(value_input, round_to)

    else:
        return 0

# ===== Mandatory breaks for Truck =====

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


def get_calculation_time_break(time_journey: float):

    '''
    Function to calculate mandatory breaks for Truck driver
    Hours are set based on law
    '''

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


# ===== Charts =====
def create_pie_chart(df: pd.DataFrame, title: str) -> Figure:
    
    fig_pie = px.pie(
        df, 
        names = "Result",
        values = "Number",
        title = title,
        color = "Result",
        color_discrete_map={'Available':'rgba(0, 105, 0, 0.8)','Not available':'rgba(175, 175, 175, 0.66)',}
        )
    
    fig_pie.update_traces(texttemplate="%{percent:.2%}")
    fig_pie.update_layout(showlegend = False)

    return fig_pie


def build_pie_chart(list_cities: list, list_cities_transport: list, title: str) -> Figure:

    '''
    - Function called specifically from VISUALIZATION STEPS st.plotly_chart
    - Combines multiple steps 
        - count len() of lists 
        - created DF
        - passing the DF to another function to build figures

    - this customized functions saves a need to create multiple variables in main.py and returns fig
    '''

    count_list_cities = len(list_cities)
    count_list_cities_transport = len(list_cities_transport)

    difference = count_list_cities - count_list_cities_transport

    df = pd.DataFrame({
                "Number" : [count_list_cities_transport , difference],
                "Result" : ["Available", "Not available",]
                })
    
   
    # Calling function for pie chart
    fig_pie = create_pie_chart(df, title)

    return fig_pie


# ===== UI functions ======
def ui_country_selector(city_options: dict, column, label: str, key_name: str) -> tuple[str, str]:

    country = column.radio(
        label,
        options=sorted([x.upper() for x in city_options.keys()])
    )

    country_code = country.lower()
    country_code_upper = country_code.upper()

    cities = city_options[country_code]

    city = column.selectbox(
        "City:",
        cities,
        key=key_name
    )

    return country_code, city, country_code_upper


def ui_door_to_door_selector(dtd_options: dict, selected_transport: str, key: str) -> str:

    selected_transport = selected_transport.lower()
    options = dtd_options[selected_transport]

    selected_value = st.radio(
        label=" ",
        options=options,
        index=0,
        horizontal=True,
        label_visibility= "collapsed",
        key= key
    )

    return selected_value


def ui_transport_offer() -> int:

    '''
    - Provide UI radio button with options 
    - Determin/retrun lookup value accroding to radio button selection
    '''

    options_dict = {
        "1 day" : 24,
        "2 days" : 48,
        "5 days" : 120,
        "7 days" : 168
    }

    options = [x for x in options_dict.keys()]

    selected_value = st.radio(
        "Customer needs to approve the transport offer till:", 
        options= options,
        horizontal = True,
        label_visibility = "collapsed",
        index = 1,
        key="key_radio_offer_approve_till"
    )

    return options_dict[selected_value], selected_value



def ui_input_formatter(value: float) -> str:

    '''
    Input formatter for UI purposes 
     - Function helping to see number insterted with with split 1_000_000 
     - Input comes as int -> change to str -> value as a list -> reverse -> for loop: after every 3rd item add ' '  & 'index != b_len' this prevents to add ' ' space in case that number has 3, 6, 9... numbers. If the condition not there, outcome: ' 100 000', if there '100 000'. -> again reverse of the list -> list back to string -> visualization on user screen
    '''
            
    a = str(value)
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


def ui_determin_singular_plural(time_input: float) -> str:

    if time_input >= 2:
        return 'hours'

    else:
        return 'hour'


# ===== Date time functions =====
def adjust_delivery_time(dt):

    hour = dt.hour

    # Must be firt TIME/HOURS determintaion if move to the next day or not - this was Bug (in case that first date condition and then time condition -> the it can happen that Friday  will be adjusted to Satruday and OVERALL rule is: 

    #  - Delivery Monday: 10:00 - 22:00
    #  - Delivery Tuesday - Friday : 07:00 - 22:00
    #  - Delivery Saturday & Sunday: No delivery ->  Monday: 10:00


    # First condition, TIME/HOURS. 
    # If 22:00 - 23:59 -> move to 07:00 next day
    # If 00:00 - 06:59 -> move to 07:00 same day 

    if hour >= 22:
        adjusted_dt = (dt + timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0)

    elif 0 <= hour < 7:
        adjusted_dt = dt.replace(hour=7, minute=0, second=0, microsecond=0)

    else:
        adjusted_dt = dt


    # Second condition. DAY 
    # If Saturday (5) -> Monday 10:00  
    # If Sunday (6) -> Monday 10:00  

    weekday = adjusted_dt.weekday()
    hour_2 = adjusted_dt.hour

    if weekday == 5:   
        adjusted_dt = (adjusted_dt + timedelta(days=2)).replace(hour=10, minute=0, second=0, microsecond=0)

    elif weekday == 6: 
        adjusted_dt = (adjusted_dt + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)

    # If Monday (0) 07:00 - 9:59 -> Monday 10:00  
    elif weekday == 0:
            if 6 < hour_2 < 10:
                adjusted_dt = dt.replace(hour=10, minute=0, second=0, microsecond=0)             

    return adjusted_dt




def delivery_date_time(overall_time, agreed_till):

    # get actual time in Europe
    date_time_europe = datetime.now(ZoneInfo(f"Europe/Prague"))
    offset_to_utc = int(date_time_europe.utcoffset().total_seconds() / 3600)

    europe_date_part = date_time_europe.date()  
    europe_date_part = europe_date_part.strftime("%d-%b-%y")

    europe_time_part = date_time_europe.time()   
    europe_time_part = europe_time_part.strftime("%H:%M")

    #gmt time - for delta purpose
    gmt = time.gmtime()
    gmt_dt = datetime(
    gmt.tm_year, gmt.tm_mon, gmt.tm_mday,
    gmt.tm_hour, gmt.tm_min, gmt.tm_sec,
    tzinfo=timezone.utc
    )

    # Delta 
    delta = timedelta(hours = (overall_time + offset_to_utc + agreed_till))
    delivery_dt = gmt_dt + delta

    # This part helps to change time delivery in case of time between 22:00 - 06:59
    delivery_dt = adjust_delivery_time(delivery_dt)

    #formating for screen visualization
    delivery_dt_formated = delivery_dt.strftime("%A - %d-%b-%y by %H:%M")

    # Customer to approve till
    customer_approve_till =  date_time_europe + timedelta(hours = agreed_till)
    customer_approve_date = customer_approve_till.date() 
    customer_approve_time = customer_approve_till.time() 

    customer_approve_date = customer_approve_date.strftime("%d-%b-%y")
    customer_approve_time = customer_approve_time.strftime("%H:%M")


    return delivery_dt, delivery_dt_formated, date_time_europe, europe_date_part, europe_time_part, customer_approve_date, customer_approve_time


# Date time function  -> to determin time CET or CEST
def determin_cet_cest(delivery_dt):

    offset_delivery = delivery_dt.replace(tzinfo = ZoneInfo("Europe/Prague"))
    offset_hours = int(offset_delivery.utcoffset().total_seconds() / 3600)

    if offset_hours == 1:
        cet_cest = 'CET'

    elif offset_hours == 2:
        cet_cest = 'CEST'

    else:
        cet_cest = ''

    return cet_cest

# ===== Validations =====
def input_validation(from_city: str, to_city: str):
    if from_city == to_city:
        st.warning("City From and To is the same -> They need to be different")
        st.stop()
    
    else:
        pass


def input_validation_shipment_value(shipment_value: int, check_isurance: bool, check_fragile: bool, check_danger: bool):
    
    if (check_isurance or check_fragile or check_danger is True) and shipment_value == None:
        st.warning("You didn't provide **Shipment value**. Please go up and provide.")
        st.stop() 
    
    else:
        pass