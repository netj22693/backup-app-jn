import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta
from Subpages.F7_DB_insert import save_to_db_main_stream
from Subpages.F7_DB_mapping import mapping_transport_type, mapping_service, mapping_time_zone, mapping_currency, mapping_agreed_till
from Subpages.F7_PDF import create_pdf
from Subpages.F7_UI_image_generator import provide_ui_image_path, provide_ui_color_coding_image, show_ui_transport_flow
from Subpages.F7_input_data import dataset_cities, correction_list_data, criteria_dict, price_dict, dtd_options_dict, dtd_calculation_values_dict, sla_dict, extra_service_dict, UNIT_DISTANCE, TRANSPORT_SPEED, ROUND_TO
from Subpages.F7_Go_green import call_go_green
from Subpages.F7_operational_functions import db_connection, create_offer_number, api_get_rate, create_df_cost_trend, create_df_extra_time, create_list_transport, create_df_default_costs, determin_square_price_per_rate, get_list_cities_if_transport_available, create_df_transport_overview, get_list_cities, build_pie_chart, delivery_date_time, create_pie_chart, ui_country_selector, get_currency_option, get_list_available_transport_based_on_selected_cities, get_price_per_square, create_df_particular_transport_overview, get_price_changed_per_service_type, get_extra_time_per_service_sla, ui_input_formatter, ui_door_to_door_selector, ui_transport_offer, ui_determin_singular_plural, get_prices_extra_services, input_validation, input_validation_shipment_value, get_coordinates, L0_is_in_correction_list, get_calculation_price_distance, get_calculation_price_distance_air, get_calculation_delivery_time, get_door_to_door_time_truck, get_door_to_door_time_train_airplane, get_calculation_time_break, get_door_to_door_cost_and_distance, determin_cet_cest, format_transport_value, format_transport_value_using_zero


# ============================================================
# ---------------- Data input creation for UI ----------------
# ============================================================

# Input creation - variables
list_transport = create_list_transport(price_dict)

extra_time_df = create_df_extra_time(sla_dict, list_transport)

# API call - get exhange rates
usd_to_czk_rate, usd_to_eur_rate = api_get_rate()


# Creation of DFs per currency for UI purposes
criteria_dataset_kc = create_df_cost_trend("kc", criteria_dict)
criteria_dataset_eur = create_df_cost_trend("eur", criteria_dict)


price_list = {

    "koruna" : {
        "Truck" : determin_square_price_per_rate(price_dict, criteria_dict, "kc", 'truck', usd_to_czk_rate),
        "Train" : determin_square_price_per_rate(price_dict, criteria_dict, "kc", 'train', usd_to_czk_rate),
        "Airplane" : determin_square_price_per_rate(price_dict, criteria_dict, "kc", 'airplane', usd_to_czk_rate)
        },
    "euro" : {
        "Truck" : determin_square_price_per_rate(price_dict, criteria_dict, "eur", 'truck', usd_to_eur_rate),
        "Train" : determin_square_price_per_rate(price_dict, criteria_dict, "eur", 'train', usd_to_eur_rate),
        "Airplane" : determin_square_price_per_rate(price_dict, criteria_dict, "eur", 'airplane', usd_to_eur_rate)
    }
}

# Lists and counts for UI widgets and Statistic charts   
train_at, count_train_at = get_list_cities_if_transport_available(dataset_cities, 'at', 'train')
train_cz, count_train_cz = get_list_cities_if_transport_available(dataset_cities, 'cz', 'train')
train_de, count_train_de = get_list_cities_if_transport_available(dataset_cities, 'de', 'train')
train_pl, count_train_pl = get_list_cities_if_transport_available(dataset_cities, 'pl', 'train')
train_sk, count_train_sk = get_list_cities_if_transport_available(dataset_cities, 'sk', 'train')


air_at, count_air_at = get_list_cities_if_transport_available(dataset_cities, 'at', 'air')
air_cz, count_air_cz = get_list_cities_if_transport_available(dataset_cities, 'cz', 'air')
air_de, count_air_de = get_list_cities_if_transport_available(dataset_cities, 'de', 'air')
air_pl, count_air_pl = get_list_cities_if_transport_available(dataset_cities, 'pl', 'air')
air_sk, count_air_sk = get_list_cities_if_transport_available(dataset_cities, 'sk', 'air')


list_at_az, count_list_at = get_list_cities(dataset_cities, 'at')
list_cz_az, count_list_cz = get_list_cities(dataset_cities, 'cz')
list_de_az, count_list_de = get_list_cities(dataset_cities, 'de')
list_pl_az, count_list_pl = get_list_cities(dataset_cities, 'pl')
list_sk_az, count_list_sk = get_list_cities(dataset_cities, 'sk')


# Note: in the current business logic Truck is available in every city as mode of transport
count_truck_cz = count_list_cz
count_truck_sk = count_list_sk
count_truck_at = count_list_at
count_truck_de = count_list_de
count_truck_pl = count_list_pl

# Difference between number of cities in each country(overall) minus number fo cities based on particular transport -> For Static charts
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


# DFs for pie charts 
data_pie_truck_overall = pd.DataFrame({
    "Number" : [
        (count_truck_cz + count_truck_sk + count_truck_at + count_truck_de + count_truck_pl),
        (diff_truck_cz + diff_truck_sk + diff_truck_at + diff_truck_de + diff_truck_pl )],
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






# ============================================================
# ---------------- UI top part of the screen  ----------------
# ============================================================

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
        st.dataframe(create_df_transport_overview(dataset_cities, 'cz'))
    
    with tab_co2:
        st.write("- **Slovakia:**")
        ''
        st.image("Pictures/Function_7/F7_cities_sk.svg", width= 520)
        ''        
        st.dataframe(create_df_transport_overview(dataset_cities, 'sk'))

    with tab_co3:
        st.write("- **Austria:**")
        ''
        st.image("Pictures/Function_7/F7_cities_at.svg", width= 520)
        ''
        st.dataframe(create_df_transport_overview(dataset_cities, 'at'))

    with tab_co4:
        st.write("- **Germany:**")
        ''
        st.image("Pictures/Function_7/F7_cities_de.svg", width= 420)
        ''
        st.dataframe(create_df_transport_overview(dataset_cities, 'de'))

    with tab_co5:
        st.write("- **Poland:**")
        ''
        st.image("Pictures/Function_7/F7_cities_pl.svg", width= 420)
        ''
        st.dataframe(create_df_transport_overview(dataset_cities, 'pl'))



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


    fig_pie_truck_overall = create_pie_chart(data_pie_truck_overall, "Truck")
    fig_pie_train_overall = create_pie_chart(data_pie_train_overall, "Train")
    fig_pie_air_overall = create_pie_chart(data_pie_air_overall, "Airplane")




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
    fig_cz_sk.update_layout(title = "Transport type availability - Country split")


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


    # Changed deprication  - Here I defined the config based on new rules
    config_chart = {
       "template": "streamlit" 
    }

    with tab1:
        with st.container(border=True):
            st.plotly_chart(fig_cz_sk, config=config_chart)
           
  
             
    with tab2:
        with st.container(border=True):
            st.plotly_chart(fig_overall, config=config_chart)



    with tab3:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(fig_pie_truck_overall, config=config_chart)
            col_stat_2.plotly_chart(fig_pie_train_overall, config=config_chart)
            col_stat_3.plotly_chart(fig_pie_air_overall, config=config_chart)
            

    # CZ
    with tab4:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(build_pie_chart(list_cz_az, list_cz_az, "CZ Truck"), config=config_chart)
            col_stat_2.plotly_chart(build_pie_chart(list_cz_az, train_cz, "CZ Train"), config=config_chart)
            col_stat_3.plotly_chart(build_pie_chart(list_cz_az, air_cz, "CZ Airplane"), config=config_chart)

    # SK
    with tab5:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(build_pie_chart(list_sk_az, list_sk_az, "SK Truck"), config=config_chart)
            col_stat_2.plotly_chart(build_pie_chart(list_sk_az, train_sk, "SK Train"), config=config_chart)
            col_stat_3.plotly_chart(build_pie_chart(list_sk_az, air_sk, "SK Airplane"))

    # AT
    with tab6:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(build_pie_chart(list_at_az, list_at_az, "AT Truck"), config=config_chart)
            col_stat_2.plotly_chart(build_pie_chart(list_at_az, train_at, "AT Train"), config=config_chart)
            col_stat_3.plotly_chart(build_pie_chart(list_at_az, air_at, "AT Airplane"), config=config_chart)

    # DE
    with tab7:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(build_pie_chart(list_de_az, list_de_az, "DE Truck"), config=config_chart)
            col_stat_2.plotly_chart(build_pie_chart(list_de_az, train_de, "DE Train"), config=config_chart)
            col_stat_3.plotly_chart(build_pie_chart(list_de_az, air_de, "DE Airplane"), config=config_chart)

    # PL
    with tab8:
        with st.container(border=True):
            col_stat_1, col_stat_2, col_stat_3 = st.columns(3, gap = "large")
            col_stat_1.plotly_chart(build_pie_chart(list_pl_az, list_pl_az, "PL Truck"), config=config_chart)
            col_stat_2.plotly_chart(build_pie_chart(list_pl_az, train_pl, "PL Train"), config=config_chart)
            col_stat_3.plotly_chart(build_pie_chart(list_pl_az, air_pl, "PL Airplane"), config=config_chart) # Changed deprication



            
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
        st.dataframe(criteria_dataset_kc, hide_index=True)
        ''

        st.write("Overview:")
        st.write("""
                - These **1-unit** costs per transport type have been set for **default** rate ( 21 <= x < 22 ) for **Standard** delivery service
                """)
        st.caption(f"**1 unit is approximatelly ~ {UNIT_DISTANCE} km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")

        col_r3,col_r4 = st.columns(2)
        col_r3.dataframe(create_df_default_costs(price_dict, list_transport, "kc", "Koruna"), hide_index=True, width='stretch')

        st.write("""
                - In case that the **rate is in** this range the application calculates with these **default** values
                - In case that the **rate is different** the relevant % increas/decrease is calculated **from the default values**
                """)


    with tab_c2:
        st.write("###### SK, AT, DE, PL - euro:")
        st.dataframe(criteria_dataset_eur, hide_index=True)
        ''

        st.write("Overview:")
        st.write("""
                - These **1-unit** costs per transport type have been set for **default** rate ( 0.82 <= x < 0.87 ) for **Standard** delivery service
                """)
        st.caption(f"**1 unit is approximatelly ~ {UNIT_DISTANCE} km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")


        col_r3,col_r4 = st.columns(2)
        col_r3.dataframe(create_df_default_costs(price_dict, list_transport, "eur", "euro"), hide_index=True, width='stretch')

        st.write("""
                - In case that the **rate is in** this range the application calculates with these **default** values
                - In case that the **rate is different** the relevant % increas/decrease is calculated **from the default values**
                """)

# Filters 
''
''
''
city_options = {
    "cz": list_cz_az,
    "sk": list_sk_az,
    "at": list_at_az,
    "de": list_de_az,
    "pl": list_pl_az,
}

col1, col2 = st.columns(2, gap="large")

from_country, from_city, country_code_from = ui_country_selector(
    city_options,
    col1,
    "Country from:",
    "key_select_box_from"
)

to_country, to_city, country_code_to = ui_country_selector(
    city_options,
    col2,
    "Country to:",
    "key_select_box_to"
)


currency = get_currency_option(from_country,to_country)

''
''
''
selected_currency = st.radio(
    "Currency:",
    currency
)


transport_options_list = get_list_available_transport_based_on_selected_cities(dataset_cities, from_country, to_country, from_city,to_city)

# UI
''
selected_transport = st.radio("Transport type:", transport_options_list)



# Calculation of price per square based on selected transport -> influencing UI
price_square = get_price_per_square(price_list, selected_currency,selected_transport)

price_square_tab2_truck = get_price_per_square(price_list, selected_currency, 'Truck')
price_square_tab2_train = get_price_per_square(price_list, selected_currency, 'Train')
price_square_tab2_air = get_price_per_square(price_list, selected_currency, 'Airplane')



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
    st.write(f"""- Average speed: **{TRANSPORT_SPEED['truck']} km/h**""")
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
    st.write(f"""- Average speed: **{TRANSPORT_SPEED['train']} km/h**""")
    st.write("""
    -   Train does **not need breaks** for the driver (in comparison with Truck)
        - The transport planning includes also **change of the drivers**, if it is that long
        - Train jurney is **not** interrupted by mandatory breaks  
    """)

    st.write("""- But is **less flexible** - Only some cities connected by rails""")


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
        st.dataframe(create_df_particular_transport_overview(train_cz, "City CZ"))

    with tab_t2:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_sk.svg", width = 460)
        ''
        st.dataframe(create_df_particular_transport_overview(train_sk, "City SK"))

    with tab_t3:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_at.svg", width = 430)
        ''
        st.dataframe(create_df_particular_transport_overview(train_at, "City AT"))

    with tab_t4:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_de.svg", width = 360)
        ''
        st.dataframe(create_df_particular_transport_overview(train_de, "City DE"))

    with tab_t5:
        ''
        st.image("Pictures/Function_7/F7_train_cityname_pl.svg", width = 410)
        ''
        st.dataframe(create_df_particular_transport_overview(train_pl, "City PL"))




with st.expander("Airplane", icon=":material/travel:"):
    ''
    st.write(f"""- Average speed: **{TRANSPORT_SPEED['airplane']} km/h**""")
    st.write("""- Very expensive but fast -> Beneficial for time critical goods/transports""")
    st.write("""- Only some cities connected""")
    ''

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
        st.dataframe(create_df_particular_transport_overview(air_cz, "City CZ"))

    with tab_a2:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_sk.svg", width = 460)
        ''
        st.dataframe(create_df_particular_transport_overview(air_sk, "City SK"))

    with tab_a3:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_at.svg", width = 430)
        ''
        st.dataframe(create_df_particular_transport_overview(air_at, "City AT"))

    with tab_a4:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_de.svg", width = 360)
        ''
        st.dataframe(create_df_particular_transport_overview(air_de, "City DE"))

    with tab_a5:
        ''
        st.image("Pictures/Function_7/F7_air_cityname_pl.svg", width = 410)
        ''
        st.dataframe(create_df_particular_transport_overview(air_pl, "City PL"))


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


if urgency  == 'Express' or urgency == 'Slow':

    price_square = get_price_changed_per_service_type(sla_dict, price_square, selected_transport, urgency)

    # TAB 2 values
    price_square_tab2_truck = get_price_changed_per_service_type(sla_dict, price_square_tab2_truck, 'Truck', urgency)
    price_square_tab2_train = get_price_changed_per_service_type(sla_dict, price_square_tab2_train, 'Train', urgency)
    price_square_tab2_air = get_price_changed_per_service_type(sla_dict, price_square_tab2_air, 'Airplane', urgency) 


# IMPORTANT: Airplane has a different way of calculating price per square
if selected_transport == 'Airplane':
    price_square = price_square / UNIT_DISTANCE


# 09-Sep-2025 - tab2 final - the logic upper "if air" here to happen no matter what transport type selected  
price_square_tab2_air = price_square_tab2_air / UNIT_DISTANCE



# Get values of extra time needed, accrodingly to selected transport mode + for all transports for TAB 2 logic
extra_time = get_extra_time_per_service_sla(sla_dict, selected_transport, urgency)

extra_time_tab2_truck = get_extra_time_per_service_sla(sla_dict, 'Truck', urgency)
extra_time_tab2_train = get_extra_time_per_service_sla(sla_dict, 'Train', urgency)
extra_time_tab2_air = get_extra_time_per_service_sla(sla_dict, 'Airplane', urgency)



# Build of the extra time string for UI purpose
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
    st.write(f" - Unit price for distance calculation: **{(price_square * UNIT_DISTANCE):,.2f}** {selected_currency}")


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
    st.write(f"- **1 unit is approximatelly ~ {UNIT_DISTANCE} km** (but not always - there are some variables/coeficients making calculation corrections, depending on case City A to City B)")
    st.write(f"- If the distance is **less than** ~ {UNIT_DISTANCE} km (You travel within 1 unit), the final price is calculated as 1 unit. This also helps to keep profit for the business.  Example: Teplice <-> Most")

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


# Determintation of value/option
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


# Extra services
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
        formated_shipment_value_str = ui_input_formatter(shipment_value)
        st.write(f"- Inserted value: **{formated_shipment_value_str}** {selected_currency}.")

        money_insurance = get_prices_extra_services(extra_service_dict, shipment_value, check_isurance, 'insurance')
        money_fragile = get_prices_extra_services(extra_service_dict, shipment_value, check_fragile, 'fragile')
        money_danger  = get_prices_extra_services(extra_service_dict, shipment_value, check_danger, 'danger')

        # Bug fix 13-Aug-25 - this line prevents case when Truck/Train selected first -> danger goods checked -> change to 'Airplane' so the checked stays (even if the check box is locked) -> app used to calculate the danger value also for Airplane. Fix to make variable always 0
        if selected_transport == 'Airplane':
            money_danger = 0



else:
    shipment_value = None

    # Creating new variables as 0 
    money_insurance = 0
    money_fragile = 0
    money_danger = 0


''
''
with st.expander("Extra services - Overview", icon= ":material/info:"):

    ''
    st.write("""
    - Multiple choices can be selected
    - Note: **Airplane** - Danger goods is **not allowed**
    """)

    ''
    st.write(f"""
    - Costs:
        - Insurance extra -> **{extra_service_dict['insurance']}%** from shipment value
        - Fragile goods -> **{extra_service_dict['fragile']}%** from shipment value
        - Danger goods -> **{extra_service_dict['danger']}%** from shipment value
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

st.write(f"From city ({from_city} - {country_code_from}):")
radio_dtd_from= ui_door_to_door_selector(dtd_options_dict, selected_transport, "radio_dtd_1")

''
st.write(f"To city ({to_city} - {country_code_to}):")
radio_dtd_to = ui_door_to_door_selector(dtd_options_dict, selected_transport, "radio_dtd_2")
    

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
                width="stretch",
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

''
''
st.write("**Customer needs to approve the transport offer till:**")
agreed_till, agreed_till_str = ui_transport_offer()

st.caption("2 days set as default. Can be changed accordingly to customer's need.")


# ============================================================
# --------------- UI - Submit button -> trigger --------------
# ============================================================

''
st.write("------")
if st.button("Submit", width="stretch", icon=":material/apps:"):

    # Validation of user inputs
    input_validation(from_city,to_city)

    input_validation_shipment_value(shipment_value, check_isurance, check_fragile, check_danger)

    # Get coordinates of selected cities -> create dict
    from_big_r, from_big_c = get_coordinates(dataset_cities, from_country, from_city, 'big')
    from_small_r, from_small_c = get_coordinates(dataset_cities, from_country, from_city, 'small')

    to_big_r, to_big_c = get_coordinates(dataset_cities, to_country, to_city, 'big')
    to_small_r, to_small_c = get_coordinates(dataset_cities, to_country, to_city, 'small')


    coordinates = {
        "from": {
            "big_r": from_big_r,
            "big_c": from_big_c,
            "small_r": from_small_r,
            "small_c": from_small_c
        },
        "to": {
            "big_r": to_big_r,
            "big_c": to_big_c,
            "small_r": to_small_r,
            "small_c": to_small_c
        }
    }

 
    # Calculation of distance and price based on transport type
    if selected_transport == 'Truck' or selected_transport == 'Train':

        distance, price, result = L0_is_in_correction_list(from_city, to_city, correction_list_data, price_square, UNIT_DISTANCE)

        if result is not True:
            price, distance = get_calculation_price_distance(coordinates, price_square, UNIT_DISTANCE)


    if selected_transport == 'Airplane':

        price, distance = get_calculation_price_distance_air(from_small_r, to_small_r,from_small_c, to_small_c, price_square)


    # Calculation time journey
    time_journey  = get_calculation_delivery_time(distance,selected_transport, TRANSPORT_SPEED)

    # DTD calculation based on transport type
    if selected_transport == 'Truck':


        time_dtd_from = get_door_to_door_time_truck(dtd_calculation_values_dict, radio_dtd_from)
        time_dtd_to = get_door_to_door_time_truck(dtd_calculation_values_dict, radio_dtd_to)

        time_dtd = time_dtd_from + time_dtd_to

        time_journy_incl_dtd = time_journey + time_dtd_from + time_dtd_to

        # Manadatorz breask fro Truck driver
        time_break = get_calculation_time_break(time_journy_incl_dtd)


        # For DB purposes to cover if scenario 'Train' and 'Air' to have values/variables for insert
        transfer_time_from = 0.00
        transfer_time_to = 0.00
        truck_time_dtd_air_train_from = 0.00
        truck_time_dtd_air_train_to = 0.00


    if selected_transport == 'Train' or selected_transport == 'Airplane':

        time_dtd_from, transfer_time_from, truck_time_dtd_air_train_from = get_door_to_door_time_train_airplane(dtd_calculation_values_dict, radio_dtd_from)
        time_dtd_to, transfer_time_to, truck_time_dtd_air_train_to  = get_door_to_door_time_train_airplane(dtd_calculation_values_dict, radio_dtd_to)


        time_dtd = time_dtd_from + time_dtd_to
    
        time_journy_incl_dtd = time_journey + time_dtd_from + time_dtd_to

        # For DB purposes to cover if scenario 'Truck' to have values/variables for insert
        time_break = 0.00


    # # DTD - distance and price
    door_from_result, from_city_extra_doortdoor = get_door_to_door_cost_and_distance(dtd_calculation_values_dict, radio_dtd_from, selected_currency, selected_transport)
    door_to_result, to_city_extra_doortdoor = get_door_to_door_cost_and_distance(dtd_calculation_values_dict, radio_dtd_to, selected_currency, selected_transport)




    # ============================================================
    # --------------- Calculations for TAB 2 logic ---------------
    # ============================================================


    # Calling all the functions with Truck, Train, Air inputs

    # TAB 2 - Truck
    tab2_distance_truck, tab2_price_truck, result_correction_list_tab2_truck = L0_is_in_correction_list(from_city, to_city, correction_list_data, price_square_tab2_truck, UNIT_DISTANCE)

    if result_correction_list_tab2_truck == False:

        tab2_price_truck, tab2_distance_truck = get_calculation_price_distance(coordinates, price_square_tab2_truck, UNIT_DISTANCE)

    # TAB 2 - Train
    tab2_distance_train, tab2_price_train, result_correction_list_tab2_train = L0_is_in_correction_list(from_city, to_city, correction_list_data, price_square_tab2_train, UNIT_DISTANCE)

    if result_correction_list_tab2_train == False:

        tab2_price_train, tab2_distance_train = get_calculation_price_distance(coordinates, price_square_tab2_train, UNIT_DISTANCE)


    # TAB 2 - Airplane
    tab2_price_air, tab2_distance_air = get_calculation_price_distance_air(from_small_r, to_small_r,from_small_c, to_small_c, price_square_tab2_air)

    

    tab2_time_journey_truck  = get_calculation_delivery_time(tab2_distance_truck, 'Truck', TRANSPORT_SPEED)
    tab2_time_journey_train  = get_calculation_delivery_time(tab2_distance_train, 'Train', TRANSPORT_SPEED)
    tab2_time_journey_air  = get_calculation_delivery_time(tab2_distance_air, 'Airplane', TRANSPORT_SPEED)

    
    # Truck DTD  and Time break 
    tab2_time_dtd_from_truck = get_door_to_door_time_truck(dtd_calculation_values_dict, radio_dtd_from)
    tab2_time_dtd_to_truck = get_door_to_door_time_truck(dtd_calculation_values_dict, radio_dtd_to)

    tab2_time_dtd_truck = tab2_time_dtd_from_truck + tab2_time_dtd_to_truck

    tab2_time_journy_incl_dtd_truck = tab2_time_journey_truck + tab2_time_dtd_from_truck + tab2_time_dtd_to_truck

    tab2_time_break = get_calculation_time_break(tab2_time_journy_incl_dtd_truck)


    # Train DTD
    tab2_time_dtd_from_train, tab2_transfer_time_from_train, tab2_truck_time_dtd_from_train = get_door_to_door_time_train_airplane(dtd_calculation_values_dict, radio_dtd_from)
    tab2_time_dtd_to_train, tab2_transfer_time_to_train, tab2_truck_time_dtd_to_train = get_door_to_door_time_train_airplane(dtd_calculation_values_dict, radio_dtd_to)


    tab2_time_dtd_train = tab2_time_dtd_from_train + tab2_time_dtd_to_train

    tab2_time_journy_incl_dtd_train = tab2_time_journey_train + tab2_time_dtd_train


    # Air DTD
    tab2_time_dtd_from_air, tab2_transfer_time_from_air, tab2_truck_time_dtd_from_air = get_door_to_door_time_train_airplane(dtd_calculation_values_dict, radio_dtd_from)
    tab2_time_dtd_to_air, tab2_transfer_time_to_air, tab2_truck_time_dtd_to_air = get_door_to_door_time_train_airplane(dtd_calculation_values_dict, radio_dtd_to)

    tab2_time_dtd_air = tab2_time_dtd_from_air + tab2_time_dtd_to_air

    tab2_time_journy_incl_dtd_air = tab2_time_journey_air + tab2_time_dtd_air



    # DTD price/costs
    # Note: the function is designed to return tuple (2 variables) ->  Return price & This *_ is unpacking to ignor the rest
    tab2_door_to_result_truck, *_ = get_door_to_door_cost_and_distance(dtd_calculation_values_dict, radio_dtd_to, selected_currency, 'Truck')
    tab2_door_to_result_train, *_ = get_door_to_door_cost_and_distance(dtd_calculation_values_dict, radio_dtd_to, selected_currency, 'Train')
    tab2_door_to_result_air, *_ = get_door_to_door_cost_and_distance(dtd_calculation_values_dict, radio_dtd_to, selected_currency, 'Airplane')

    tab2_door_from_result_truck, *_ = get_door_to_door_cost_and_distance(dtd_calculation_values_dict, radio_dtd_from, selected_currency, 'Truck')
    tab2_door_from_result_train, *_ = get_door_to_door_cost_and_distance(dtd_calculation_values_dict, radio_dtd_from, selected_currency, 'Train')
    tab2_door_from_result_air, *_ = get_door_to_door_cost_and_distance(dtd_calculation_values_dict, radio_dtd_from, selected_currency, 'Airplane')


    # DB connection -> Engine + getting offer number 
    db_engine = db_connection()

    if db_engine != None:
        offer_number_generated = create_offer_number(db_engine)
    
    elif db_engine == None:
        offer_number_generated = "Error - Not possible to generate"



    # ============================================================
    # ------ UI visualization & additional calculations ----------
    # ============================================================
    ''
    ''
    st.write("##### Calculated values:")
    '' 


    tab_final_1, tab_final_2,tab_final_3 = st.tabs([
        f"Offer - {selected_transport}",
        "Analytics & Other transports",
        "Go Green - CO₂"
    ])


    # Get UI image for the particular offer 
    ui_image_path = provide_ui_image_path(selected_transport, from_city_extra_doortdoor, to_city_extra_doortdoor, time_break)
    ui_color_coding_image_path = provide_ui_color_coding_image(selected_transport, from_city_extra_doortdoor, to_city_extra_doortdoor, time_break)

    # UI transport workflow image
    ''
    with tab_final_1:
        if selected_transport == 'Truck':

            time_truck_physical_move = (time_journey + time_break + time_dtd)
            overall_time_truck = (time_journey + time_break + extra_time + time_dtd)

            #overall_time_db - for DB purpose unified variable (the same will have train and truck)
            overall_time_db = overall_time_truck 


            delivery_dt, delivery_dt_formated, date_time_europe, europe_date_part, europe_time_part, customer_approve_date, customer_approve_time, delivery_at_utc, approve_till_utc, created_utc, transport_start_utc = delivery_date_time(overall_time_truck,agreed_till, time_truck_physical_move, True)

            cet_cest_delivery = determin_cet_cest(delivery_dt)
            cet_cest_now = determin_cet_cest(date_time_europe)



            ''
            st.write(f"""
                - Offer number: **{offer_number_generated}**
                - Offer created: **{europe_date_part} - {europe_time_part} {cet_cest_now}**
                - Customer to approve till: **{customer_approve_date} - {customer_approve_time} {cet_cest_now}** ({agreed_till_str})
            """)


            # UI transport workflow image
            ''
            show_ui_transport_flow(ui_image_path, ui_color_coding_image_path)


            ''
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

            with st.container(border=True):
                st.write(f"**{overall_time_truck:.2f} {ui_determin_singular_plural(overall_time_truck)}**")



            st.write("- **Expected delivery:**")
            with st.container(border=True):
                st.write(f"**{delivery_dt_formated} - {cet_cest_delivery}**")
            
            with st.expander("Info", icon=":material/help:"):

                tab_info_1, tab_info_2 = st.tabs([
                    "How",
                    "DTF - Delivery Time Frame"
                ])


                tab_info_1.write(f"""
                    - Calculated based on:
                        - Current time and date: **{europe_date_part} - {europe_time_part} - {cet_cest_now}**
                        - Overall end-to-end delivery: **{overall_time_truck:.2f} {ui_determin_singular_plural(overall_time_truck)}**
                        - Time till the customer needs to approve the offer: **{agreed_till} hours** ({agreed_till_str})
                """)    

                tab_info_1.write("- **If the result does not fit to DTF (Delivery Time Frame) -> it is asjusted accordingly the DTF rules**")


                tab_info_2.write(f"""
                    - Monday: **10:00 - 22:00**
                    - Tuesday - Friday : **07:00 - 22:00**
                    - Saturday & Sunday: No delivery ->  **Monday: 10:00**
                """)   
                
                tab_info_2.write("- In case that **calculated Expected delivery time** is **not** in these time frames -> **the delivery time is adjusted to fit into these**")




        elif selected_transport == 'Train' or 'Airplane':

            time_train_air_physical_move = time_journey + time_dtd
            overall_time_train_air = time_journey + extra_time + time_dtd

            #overall_time_db - for DB purpose unified variable (the same will have train and truck)
            overall_time_db = overall_time_train_air

            delivery_dt, delivery_dt_formated, date_time_europe, europe_date_part, europe_time_part, customer_approve_date, customer_approve_time, delivery_at_utc, approve_till_utc, created_utc, transport_start_utc = delivery_date_time(overall_time_train_air,agreed_till, time_train_air_physical_move, True)

            cet_cest_delivery = determin_cet_cest(delivery_dt)
            cet_cest_now = determin_cet_cest(date_time_europe)



            ''
            st.write(f"""
                - Offer number: **{offer_number_generated}**
                - Offer created: **{europe_date_part} - {europe_time_part} {cet_cest_now}**
                - Customer to approve till: **{customer_approve_date} - {customer_approve_time} {cet_cest_now}** ({agreed_till_str})
            """)

            # UI transport workflow image
            ''
            show_ui_transport_flow(ui_image_path, ui_color_coding_image_path)

            ''
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

            with st.container(border=True):
                st.write(f"**{overall_time_train_air:.2f} {ui_determin_singular_plural(overall_time_train_air)}**")
        


            st.write("- **Expected delivery:**")
            with st.container(border=True):
                st.write(f"**{delivery_dt_formated} - {cet_cest_delivery}**")
            
            with st.expander("Info", icon=":material/help:"):

                tab_info_ta_1, tab_info_ta_2 = st.tabs([
                    "How",
                    "DTF - Delivery Time Frame"
                ])


                tab_info_ta_1.write(f"""
                    - Calculated based on:
                        - Current time and date: **{europe_date_part} - {europe_time_part} - {cet_cest_now}**
                        - Overall end-to-end delivery: **{overall_time_train_air:.2f} {ui_determin_singular_plural(overall_time_train_air)}**
                        - Time till the customer needs to approve the offer: **{agreed_till} hours** ({agreed_till_str})
                """)    

                tab_info_ta_1.write("- **If the result does not fit to DTF (Delivery Time Frame) -> it is asjusted accordingly the DTF rules**")



                tab_info_ta_2.write(f"""
                    - Monday: **10:00 - 22:00**
                    - Tuesday - Friday : **07:00 - 22:00**
                    - Saturday & Sunday: No delivery ->  **Monday: 10:00**
                """)   
                
                tab_info_ta_2.write("- In case that calculated delivery time is **not** in these time frames -> **the delivery time is adjsuted to fit into these**")


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

            final_price = price + money_insurance + money_fragile + money_danger + door_to_result + door_from_result

            st.write(f"**{final_price:,.2f} {selected_currency}**")



    # TAB 2
    with tab_final_2:

        transport_options_list_str = ', '.join(transport_options_list)

        ''
        st.write(f"""
            - Transport: **{from_city} ({country_code_from}) - {to_city} ({country_code_to})** 
            - Available transport options: **{transport_options_list_str}**""")

        if len(transport_options_list) == 1:
            st.warning(f"For {from_city} ({country_code_from}) - {to_city} ({country_code_to}) there is **only {transport_options_list_str}** available -> **no other transport option**")

        with st.expander("Color-coding charts", icon= ":material/help:"):
            st.image("Pictures/Function_7/F7_tab2_colorcoding.svg")
            pass


        # Truck - current logic has Truck available in every city -> no need to call function
        tab2_time_journey_truck_rounded = round(tab2_time_journey_truck, ROUND_TO)
        tab2_time_journey_train_rounded = format_transport_value(transport_options_list, 'Train', tab2_time_journey_train, ROUND_TO)
        tab2_time_journey_air_rounded = format_transport_value(transport_options_list, 'Airplane', tab2_time_journey_air, ROUND_TO)

         # Truck - current logic has Truck available in every city -> no need to call function
        tab2_price_truck_rounded = round(tab2_price_truck, ROUND_TO)
        tab2_price_train_rounded = format_transport_value(transport_options_list, 'Train', tab2_price_train, ROUND_TO)
        tab2_price_air_rounded = format_transport_value(transport_options_list, 'Airplane', tab2_price_air, ROUND_TO)


        df_tab2_transport = pd.DataFrame({
            "Transport type" : ['Truck','Train','Airplane'],

            "Distance (km)" : [
                # Truck - current logic has truck available in every city -> no need to call function
                round(tab2_distance_truck, ROUND_TO),
                # Train
                format_transport_value(transport_options_list, 'Train', tab2_distance_train, ROUND_TO),
                # Airplane
                format_transport_value(transport_options_list, 'Airplane', tab2_distance_air, ROUND_TO)
            ],

            "Time (hours)" : [tab2_time_journey_truck_rounded, tab2_time_journey_train_rounded, tab2_time_journey_air_rounded],

            f"Price ({selected_currency})" : [tab2_price_truck_rounded, tab2_price_train_rounded, tab2_price_air_rounded],
        })


        df_tab2_transport.drop(df_tab2_transport.loc[df_tab2_transport['Time (hours)']== 'n/a'].index, inplace=True)

        df_tab2_transport_styled = df_tab2_transport.style.format({
            "Distance (km)": "{:,.2f}",
            "Time (hours)" : "{:.2f}",
            f"Price ({selected_currency})": "{:,.2f}",
        })


       
        tab2_door_result_truck = tab2_door_from_result_truck + tab2_door_to_result_truck
        tab2_door_result_train = tab2_door_from_result_train + tab2_door_to_result_train
        tab2_door_result_air = tab2_door_from_result_air + tab2_door_to_result_air

        tab2_door_result_train = format_transport_value(transport_options_list, 'Train', tab2_door_result_train, ROUND_TO)
        tab2_door_result_air = format_transport_value(transport_options_list, 'Airplane', tab2_door_result_air, ROUND_TO)


        df_tab2_dtd = pd.DataFrame({
            "Transport type" : ['Truck','Train','Airplane'],

            "Time (hours)**" : [
                # Truck - current logic has truck available in every city -> no need to call function
                tab2_time_dtd_truck,

                # Train
                format_transport_value(transport_options_list, 'Train', tab2_time_dtd_train, ROUND_TO),

                # Airplane
                format_transport_value(transport_options_list, 'Airplane', tab2_time_dtd_air, ROUND_TO)
                ],


            f"Price ({selected_currency})" : [tab2_door_result_truck, tab2_door_result_train, tab2_door_result_air],
        })

        df_tab2_dtd.drop(df_tab2_dtd.loc[df_tab2_dtd['Time (hours)**']== 'n/a'].index, inplace=True)

        df_tab2_dtd = df_tab2_dtd.style.format({
            "Time (hours)**" : "{:.2f}",
            f"Price ({selected_currency})": "{:,.2f}",
        })



        #TAB 2 time
        tab2_overall_time_truck = tab2_time_journey_truck_rounded + tab2_time_break + extra_time_tab2_truck + tab2_time_dtd_truck
        tab2_overall_time_train = tab2_time_journey_train + extra_time_tab2_train + tab2_time_dtd_train
        tab2_overall_time_air = tab2_time_journey_air + extra_time_tab2_air + tab2_time_dtd_air


        tab2_overall_time_truck_rounded = round(tab2_overall_time_truck, ROUND_TO)
        tab2_overall_time_train_rounded = format_transport_value(transport_options_list, 'Train', tab2_overall_time_train, ROUND_TO)
        tab2_overall_time_air_rounded = format_transport_value(transport_options_list, 'Airplane', tab2_overall_time_air, ROUND_TO)



        # TAB 2 price
        tab2_price_overall_truck = round(tab2_price_truck + money_insurance + money_fragile + money_danger + tab2_door_from_result_truck + tab2_door_to_result_truck, ROUND_TO)
        tab2_price_overall_train = round(tab2_price_train + money_insurance + money_fragile + money_danger + tab2_door_from_result_train + tab2_door_to_result_train, ROUND_TO)

        # 10-Sep-25: Bug fix - air does NOT include '+ money_danger'because it is not allowed to trnasport dnager goods in airplane. Bug detail: this prevents from case when user selects 'danger goods - True' when having Truck or Train and then switch to Airplane (bug was also counting with the variable which is not following business logic)
        tab2_price_overall_air = round(tab2_price_air + money_insurance + money_fragile + tab2_door_from_result_air + tab2_door_to_result_air, ROUND_TO)


        tab2_price_overall_train = format_transport_value(transport_options_list, 'Train', tab2_price_overall_train, ROUND_TO)
        tab2_price_overall_air = format_transport_value(transport_options_list, 'Airplane', tab2_price_overall_air, ROUND_TO)



        # ============================================================
        # -------------- Calculations for TAB 2 charts ---------------
        # ============================================================

        # Data -> Variables for charts -> in case that transport type not available for combination of cities -> make the variable as 0. 

        # 1. Transfer time - From A   - Train, Air
        tab2_transfer_time_from_train_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Train', tab2_transfer_time_from_train, ROUND_TO)
        tab2_transfer_time_from_air_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', tab2_transfer_time_from_air, ROUND_TO)


        # 2. Time - From A  - Train, Air
        tab2_truck_time_dtd_from_train_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Train', tab2_truck_time_dtd_from_train, ROUND_TO)
        tab2_truck_time_dtd_from_air_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', tab2_truck_time_dtd_from_air, ROUND_TO)


        # 3. Transfer time - From B - Train, Air
        tab2_transfer_time_to_train_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Train', tab2_transfer_time_to_train, ROUND_TO)
        tab2_transfer_time_to_air_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', tab2_transfer_time_to_air, ROUND_TO)

       
        # 4. Time - From B - Train, Air
        tab2_truck_time_dtd_to_train_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Train', tab2_truck_time_dtd_to_train, ROUND_TO)
        tab2_truck_time_dtd_to_air_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', tab2_truck_time_dtd_to_air, ROUND_TO)


        # 5. Transfer time sum (from + to) 
        tab2_train_transf_sum = tab2_transfer_time_from_train_adj_r0 + tab2_transfer_time_to_train_adj_r0
        tab2_air_transf_sum = tab2_transfer_time_from_air_adj_r0 + tab2_transfer_time_to_air_adj_r0


        # 6. Price - dtd from (A)  - Train, Air
        tab2_door_from_result_train_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Train', tab2_door_from_result_train, ROUND_TO)
        tab2_door_from_result_air_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', tab2_door_from_result_air, ROUND_TO)


        # 7. Price - dtd to (B)  - Train, Air
        tab2_door_to_result_train_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Train', tab2_door_to_result_train, ROUND_TO) 
        tab2_door_to_result_air_adj_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', tab2_door_to_result_air, ROUND_TO)


        # 8. sum of extra services (air has not money_danger as not allowed to transport in Air)
        sum_extra_services_truck_train = money_fragile + money_insurance + money_danger
        sum_extra_services_air = money_fragile + money_insurance

        tab2_extra_services_train_r0 = format_transport_value_using_zero(transport_options_list, 'Train', sum_extra_services_truck_train, ROUND_TO)  
        tab2_sum_extra_services_air_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', sum_extra_services_air, ROUND_TO)


        # 9. sum costs distance + dtd 
        tab2_dist_dtd_truck = tab2_door_result_truck + tab2_price_truck_rounded
        tab2_dist_dtd_train = tab2_door_result_train + tab2_price_train_rounded
        tab2_dist_dtd_air = tab2_door_result_air + tab2_price_air_rounded

        tab2_dist_dtd_train_r0 = format_transport_value_using_zero(transport_options_list, 'Train', tab2_dist_dtd_train, ROUND_TO)  
        tab2_dist_dtd_air_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', tab2_dist_dtd_air, ROUND_TO)


        # 10. Overall time (Distance + DTD + Transfer + Breaks) - Service time  -> Time of physical movement of the shipment 
        tab2_ov_time_truck = tab2_overall_time_truck - extra_time_tab2_truck
        tab2_ov_time_train = tab2_overall_time_train - extra_time_tab2_train
        tab2_ov_time_air = tab2_overall_time_air - extra_time_tab2_air

        tab2_ov_time_train_r0 = format_transport_value_using_zero(transport_options_list, 'Train', tab2_ov_time_train, ROUND_TO) 
        tab2_ov_time_air_r0 = format_transport_value_using_zero(transport_options_list, 'Airplane', tab2_ov_time_air, ROUND_TO)


        # 11. Conditions for keeping exact same time/variable  + getting the Expected delivery also for other transport types

        if selected_transport == 'Truck':
            tab2_delivery_dt_formated_truck = delivery_dt_formated
        
        else:
            tab2_delivery_dt_truck, tab2_delivery_dt_formated_truck, tab2_date_time_europe_truck, tab2_europe_date_part_truck, tab2_europe_time_part_truck, tab2_customer_approve_date_truck, tab2_customer_approve_time_truck = delivery_date_time(tab2_overall_time_truck_rounded,agreed_till)


        if selected_transport == 'Train':
            tab2_delivery_dt_formated_train = delivery_dt_formated  

        else:
            tab2_delivery_dt_train, tab2_delivery_dt_formated_train, tab2_date_time_europe_train, tab2_europe_date_part_train, tab2_europe_time_part_train, tab2_customer_approve_date_train, tab2_customer_approve_time_train = delivery_date_time(tab2_overall_time_train,agreed_till)


        if selected_transport == 'Airplane':
            tab2_delivery_dt_formated_air = delivery_dt_formated  

        else:
            tab2_delivery_dt_air, tab2_delivery_dt_formated_air, tab2_date_time_europe_air, tab2_europe_date_part_air, tab2_europe_time_part_air, tab2_customer_approve_date_air, tab2_customer_approve_time_air = delivery_date_time(tab2_overall_time_air,agreed_till)




        df_tab2_overall_time = pd.DataFrame({
            "Transport type" : ['Truck','Train','Airplane'],
            "Time (hours)" : [tab2_overall_time_truck_rounded, tab2_overall_time_train_rounded, tab2_overall_time_air_rounded],
            f"Price ({selected_currency})" : [tab2_price_overall_truck, tab2_price_overall_train, tab2_price_overall_air],
            f"Expected delivery ({cet_cest_now})" : [tab2_delivery_dt_formated_truck, tab2_delivery_dt_formated_train ,tab2_delivery_dt_formated_air]
        })


        df_tab2_overall_time.drop(df_tab2_overall_time.loc[df_tab2_overall_time['Time (hours)']== 'n/a'].index, inplace=True)


        df_tab2_overall_time = df_tab2_overall_time.style.format({
            "Time (hours)" : "{:.2f}",
            f"Price ({selected_currency})": "{:,.2f}",
        })



        extra_time_tab2_train_adj = format_transport_value(transport_options_list, 'Train', extra_time_tab2_train, ROUND_TO)
        extra_time_tab2_air_adj = format_transport_value(transport_options_list, 'Airplane', extra_time_tab2_air, ROUND_TO)

        df_tab2_service = pd.DataFrame({
            "Transport type" : ['Truck','Train','Airplane'],
            "Time (hours)" : [extra_time_tab2_truck, extra_time_tab2_train_adj, extra_time_tab2_air_adj]
        })

        df_tab2_service.drop(df_tab2_service.loc[df_tab2_service['Time (hours)']== 'n/a'].index, inplace=True)


        tab2_truck_break_for_df = {
            "Transport type" : 'Truck',
            "Mandatory break (hours)" : tab2_time_break    
        }

        df_tab2_truck_break = pd.DataFrame(tab2_truck_break_for_df, index=[0])



        df_tab2_extra_s = pd.DataFrame({
            "Extra service" : ["Insurance extra", "Fragile goods", "Danger goods"],
            f"Price ({selected_currency})" : [money_insurance, money_fragile, money_danger],
        })

        df_tab2_extra_s = df_tab2_extra_s.style.format({
            f"Price ({selected_currency})" : "{:,.2f}",
        })



        # ============================================================
        # ------------------- TAB 2 Charts creation ------------------
        # ============================================================

        # ------- Chart - Time overall including administartion -------  
        x_transport_time = ['Truck','Train', 'Airplane']

        y_time_overall = [tab2_ov_time_truck, tab2_ov_time_train_r0, tab2_ov_time_air_r0]
        y_time_service = [extra_time_tab2_truck, extra_time_tab2_train_adj, extra_time_tab2_air_adj] 

        fig_tab2_time_o = go.Figure()


        fig_tab2_time_o.add_bar(x=x_transport_time,y=y_time_service, name= f"Administration - Service: {urgency}",
            marker=dict(
                color='rgba(187, 188, 191, 0.8)',
            )
        )
        fig_tab2_time_o.add_bar(x=x_transport_time,y=y_time_overall, name= "Transport/Delivery",
            marker=dict(
                color='rgba(0, 112, 192, 1)',
            )
        )

        fig_tab2_time_o.update_layout(barmode="relative")
        fig_tab2_time_o.update_layout(title = "Time - Overall (hours)")  


        # ------- Chart - Time overall just transports ------- 
        x_transport_time = ['Truck','Train', 'Airplane']

        y_time_overall_2 = [tab2_ov_time_truck, tab2_ov_time_train_r0, tab2_ov_time_air_r0]

        fig_tab2_time_o2 = go.Figure()

        fig_tab2_time_o2.add_bar(x=x_transport_time,y=y_time_overall_2, name= "Transport/Delivery",
            marker=dict(
                color='rgba(0, 112, 192, 1)',
            )
        )

        fig_tab2_time_o2.update_layout(barmode="relative")
        fig_tab2_time_o2.update_layout(title = "Time - Overall transport (hours)")  


        # ------- Chart - Price overall ------- 
        x_transport_price_o = ['Truck','Train', 'Airplane']

        y_price_overall = [tab2_dist_dtd_truck, tab2_dist_dtd_train_r0, tab2_dist_dtd_air_r0]
        y_price_services = [sum_extra_services_truck_train, tab2_extra_services_train_r0, tab2_sum_extra_services_air_r0 ] 

        fig_tab2_price_o = go.Figure()


        fig_tab2_price_o.add_bar(x=x_transport_price_o,y=y_price_services, name= f"Extra services",
            marker=dict(
                color='rgba(20, 19, 18, 0.8)',
            )
        )
        fig_tab2_price_o.add_bar(x=x_transport_price_o,y=y_price_overall, name= "Transport/Delivery",
            marker=dict(
                color='rgba(0, 112, 192, 1)',
            )
        )

        fig_tab2_price_o.update_layout(barmode="relative")
        fig_tab2_price_o.update_layout(title = f"Price - Overall ({selected_currency})")  


        # ============================================================
        # ------------------------- TAB 2 UI -------------------------
        # ============================================================
        ''
        ''
        with st.container(border=True):
            st.write("###### Overall Time and Price end-to-end delivery:")

            ''
            
            st.dataframe(df_tab2_overall_time, hide_index=True)

            with st.expander("Chart - Time", icon= ":material/bar_chart:"):


                tab_exp_cht_1, tab_exp_cht_2 = st.tabs([
                    "Overall",
                    "Transport without administration"
                ])


                config_chart_tab2 = {
                    "template": "streamlit"
                }

                with tab_exp_cht_1:
                    st.plotly_chart(fig_tab2_time_o, config=config_chart_tab2) # Changed deprication


                with tab_exp_cht_2:

                    col_exp_cht_1, col_exp_cht_2 = st.columns(2)

                    col_exp_cht_1.plotly_chart(fig_tab2_time_o2, config=config_chart_tab2) # Changed deprication

                    col_exp_cht_2.write("""
                    - **Time to cover the transport -> physical movement of the shipment**
                    - **Truck:** Distance + DTD + Breaks
                    - **Train:** Distance + DTD + Transfer
                    - **Airplane:** Distance + DTD + Transfer
                    """)

            with st.expander("Chart - Price", icon= ":material/bar_chart:"):
                st.plotly_chart(fig_tab2_price_o, config=config_chart_tab2) # Changed deprication



                st.write("- Note (!): Danger goods is **not allowed in Airplane** -> not counted")
                col_exp_pr_1, col_exp_pr_2 = st.columns(2)

                col_exp_pr_1.dataframe(df_tab2_extra_s, hide_index=True)



        with st.container(border=True):
            st.write("###### Detail:")
            st.write(f"- {from_city} ({country_code_from}) - {to_city} ({country_code_to})")

            st.dataframe(df_tab2_transport_styled, hide_index=True)

            col_break_1, col_break_2 = st.columns(2)
            col_break_1.dataframe(df_tab2_truck_break, hide_index=True)

            ''
            st.write(f"""
                - Door-to-Door:
                    - {from_city} ({country_code_from}): **{from_city_extra_doortdoor} km**
                    - {to_city} ({country_code_to}): **{to_city_extra_doortdoor} km**
                """)

            st.dataframe(df_tab2_dtd, hide_index=True)

            st.caption("""
            ** For **Train** and **Airplane** - includes time for transfer Truck <-> Train/Airplane
            """)

        # ============================================================
        # ---------- TAB 2 Charts creation DETAIL section ------------
        # ============================================================

        # ------- Chart Time ------- 
            x_transport = ['Truck','Train', 'Airplane']

            y_time_distance = [tab2_time_journey_truck_rounded, tab2_time_journey_train_rounded, tab2_time_journey_air_rounded]
            y_time_dtd_a = [tab2_time_dtd_from_truck,tab2_truck_time_dtd_from_train_adj_r0,tab2_truck_time_dtd_from_air_adj_r0]
            y_time_dtd_b = [tab2_time_dtd_to_truck,tab2_truck_time_dtd_to_train_adj_r0,tab2_truck_time_dtd_to_air_adj_r0]
            y_time_transfer = [0, tab2_train_transf_sum, tab2_air_transf_sum]
            y_time_break = [tab2_time_break , 0, 0]
            # y_time_service = [extra_time_tab2_truck, extra_time_tab2_train_adj, extra_time_tab2_air_adj] 

            fig_tab2_time = go.Figure()

            fig_tab2_time.add_bar(x=x_transport,y=y_time_distance, name= "Distance",
                marker=dict(
                    color='rgba(219, 238, 243, 1)',
                )
            )

            fig_tab2_time.add_bar(x=x_overall,y=y_time_dtd_a, name= f"DTD {from_city}",
                marker=dict(
                    color='rgba(254, 229, 153, 1)',
                )
            )

            fig_tab2_time.add_bar(x=x_overall,y=y_time_dtd_b, name= f"DTD {to_city}",
                marker=dict(
                    color='rgba(229, 185, 181, 1)',
                )
            )

            fig_tab2_time.add_bar(x=x_overall,y=y_time_transfer, name= f"Transfer",
                marker=dict(
                    color='rgba(235, 241, 223, 1)',
                )
            )

            fig_tab2_time.add_bar(x=x_overall,y=y_time_break, name= f"Break Truck",
                marker=dict(
                    color='rgba(248, 241, 235, 1)',
                )
            )

            fig_tab2_time.update_layout(barmode="relative")
            fig_tab2_time.update_layout(title = "Time - Distance & DTD (hours)")            


            # ------- Chart Price ------- 
            x_price_transport = ['Truck','Train', 'Airplane']

            y_price_distance = [tab2_price_truck_rounded, tab2_price_train_rounded, tab2_price_air_rounded]

            y_price_dtd_a = [tab2_door_from_result_truck,
            tab2_door_from_result_train_adj_r0,tab2_door_from_result_air_adj_r0]

            y_price_dtd_b = [tab2_door_to_result_truck,tab2_door_to_result_train_adj_r0,tab2_door_to_result_air_adj_r0]

            fig_overall_2 = go.Figure()

            fig_overall_2.add_bar(x=x_price_transport,y=y_price_distance, name= "Distance",
                marker=dict(
                    color='rgba(219, 238, 243, 1)',
                )
            )


            fig_overall_2.add_bar(x=x_overall,y=y_price_dtd_a, name= f"DTD {from_city}",
                marker=dict(
                    color='rgba(254, 229, 153, 1)',
                )
            )
            fig_overall_2.add_bar(x=x_overall,y=y_price_dtd_b, name= f"DTD {to_city}",
                marker=dict(
                    color='rgba(229, 185, 181, 1)',
                )
            )

            fig_overall_2.update_layout(barmode="relative")
            fig_overall_2.update_layout(title = f"Price - Distance & DTD ({selected_currency})")




            with st.expander("Chart - Time - Distance & DTD", icon= ":material/bar_chart:"):
                st.plotly_chart(fig_tab2_time, config=config_chart_tab2) # Changed deprication


            with st.expander("Chart - Price - Distance & DTD", icon= ":material/bar_chart:"):
                st.plotly_chart(fig_overall_2, config=config_chart_tab2) # Changed deprication



            ''
            st.write(f"- Selected service - **{urgency}**")

            col_urg_1, col_urg_2 = st.columns(2)
            col_urg_1.dataframe(df_tab2_service, width='stretch', hide_index=True)   # Changed deprication   



    with tab_final_3:

        # Calling Go Green function
        df_go_green_main_df, df_go_green_main_df_styled, df_emissions_values_db,df_emissions_values_db_styled, variables_go_green_dict_returned = call_go_green(db_engine, from_city_extra_doortdoor, to_city_extra_doortdoor, df_tab2_transport, selected_transport)


        # UI
        col1,col2 = st.columns(2)

        col1.image("Pictures/Function_7/F7_Go_green/F7_go_green_environment.svg", width=100)

        st.dataframe(df_go_green_main_df_styled, hide_index=True)

        with st.expander("Emissions", icon=":material/co2:"):
            
            st.write("- **Note:** DTD is served by **Truck** -> emissions for Truck")
            st.dataframe(df_emissions_values_db_styled, hide_index=True)
            

        # ============================================================
        # ---------- DB, PDF data preparations + mapping -------------
        # ============================================================

        # 1) OFFER table
        # Mapping      
        mapped_selected_transport = mapping_transport_type(selected_transport)
        mapped_service =  mapping_service(urgency)
        mapped_time_zone =  mapping_time_zone(cet_cest_now)
        mapped_currency =  mapping_currency(selected_currency)
        mapped_agreed_till = mapping_agreed_till(agreed_till_str)

        # Dictionary for INSERT
        variables_offer_dict = {
            "offer_id" : offer_number_generated,
            "europe_date_part" : europe_date_part, # 06-Dec-25
            "europe_time_part" : europe_time_part, # 12:04
            "customer_approve_date":customer_approve_date,
            "customer_approve_time" : customer_approve_time,
            "agreed_till_str": mapped_agreed_till,
            "selected_transport" : mapped_selected_transport,
            "service" : mapped_service,
            "time_zone" : mapped_time_zone,
            "time_overall" : overall_time_db,
            "expected_delivery" : delivery_dt_formated,
            "final_price" : final_price,
            "currency" : mapped_currency,
            "created_utc": created_utc,
            "approve_till_utc": approve_till_utc,
            "transport_start_utc": transport_start_utc,
            "delivery_at_utc": delivery_at_utc,
            "offer_state": "CREATED" # Default hardcoded state for insert
            }

        # 2) DELIVERY table 
        # Dictionary for INSERT
        variables_delivery_dict = {
            "offer_id" : offer_number_generated,
            "from_country" : country_code_from,
            "from_city" : from_city,
            "from_dtd" : from_city_extra_doortdoor,
            "to_country" : country_code_to,
            "to_city" : to_city,
            "to_dtd" : to_city_extra_doortdoor,
            "distance_length" : distance,
            "distance_time" : time_journey,
            "dtd_time" : time_dtd
        }

        # 3) COSTS table 
        # Dictionary for INSERT
        variables_costs_dict = {
            "offer_id" : offer_number_generated,
            "currency" : mapped_currency,
            "distance_cost" : price,
            "dtd_from" : door_from_result,
            "dtd_to" : door_to_result,
            "shipment_value" : shipment_value,
            "insurance" : money_insurance,
            "fragile" : money_fragile,
            "danger" : money_danger,
        }

        # 4) EXTRA_STEPS_TIME table 
        # Dictionary for INSERT
        variables_extra_steps_time_dict = {
            "offer_id" : offer_number_generated,
            "truck_breaks" : time_break,
            "shipment_transfer_dtd_from" : transfer_time_from,
            "shipment_transfer_dtd_to" : transfer_time_to,
            "dtd_truck_if_not_truck_main" : (truck_time_dtd_air_train_from + truck_time_dtd_air_train_to),
        }

        # 5) GO_GREEN table
        # Dictionary for INSERT
        offer_id = {
            "offer_id" : offer_number_generated,
        }

        variables_extra_go_green_dict = offer_id | variables_go_green_dict_returned

        # 6) STATE_CHANGE_LOG table 
        # Dictionary for INSERT
        state_change_log_dict = {
            "offer_id": offer_number_generated,
            "state_from": " ",
            "state_to": "CREATED",
            "change_note": "Created by user - Function 7",
            "timestamp_utc": created_utc
        }


        # 7) OFFER_RATING table 
        # Dictionary for INSERT
        offer_rating_dict = {
            "offer_id": offer_number_generated,
            "rating_given": False,
            "delivery_at_utc": delivery_at_utc,
            "rating_possible_till_utc": delivery_at_utc + timedelta(days=14),
        }

        # PDF 
        data_for_pdf = {
            "offer_id" : offer_number_generated,
            "europe_date_part" : europe_date_part, 
            "europe_time_part" : europe_time_part, 
            "customer_approve_date":customer_approve_date,
            "customer_approve_time" : customer_approve_time,
            "agreed_till_str": agreed_till_str,
            "selected_transport" : selected_transport,
            "service" : urgency,
            "service_time": extra_time,
            "time_zone" : cet_cest_now,
            "time_overall" : overall_time_db,
            "expected_delivery" : delivery_dt_formated,
            "final_price" : final_price,
            "currency" : selected_currency,
            "from_country" : country_code_from,
            "from_city" : from_city,
            "from_dtd" : from_city_extra_doortdoor,
            "to_country" : country_code_to,
            "to_city" : to_city,
            "to_dtd" : to_city_extra_doortdoor,
            "distance_length" : distance,
            "distance_time" : time_journey,
            "dtd_time" : time_dtd,
            "distance_cost" : price,
            "dtd_from" : door_from_result,
            "dtd_to" : door_to_result,
            "shipment_value" : shipment_value,
            "insurance" : money_insurance,
            "fragile" : money_fragile,
            "danger" : money_danger,
            "truck_breaks" : time_break,
            "shipment_transfer_dtd_from" : transfer_time_from,
            "shipment_transfer_dtd_to" : transfer_time_to,
            "dtd_truck_if_not_truck_main" : (truck_time_dtd_air_train_from + truck_time_dtd_air_train_to)
        }

        # PDF creation
        data_pdf = create_pdf(data_for_pdf, selected_transport)

    # Final button moved at the end of the code
    # Reason: the button calls save to DB function -> I need Go Green data to be saved as well
    with tab_final_1:
        ''
        ''
        st.info("""
        - Note:
            - If you want to check the **Analytics** and **Go Green** tabs, do it before this button
            - This button will **close the results**
            - **It is final step to confirm the offer -> closing the function**
            """)
        
        st.download_button(
            "Generate PDF file & Save the offer into DB",
            width="stretch",
            icon=":material/sports_score:",
            data = data_pdf,
            file_name=f"Offer_{offer_number_generated}.pdf",
            mime="application/pdf",
            on_click=lambda: save_to_db_main_stream(offer_number_generated, variables_offer_dict, variables_delivery_dict, variables_costs_dict, variables_extra_steps_time_dict, variables_extra_go_green_dict, state_change_log_dict, offer_rating_dict),
            key="key_save_button"
        )
