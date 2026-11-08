import streamlit as st
import pandas as pd
from sqlalchemy import text
from app_db_connection import db_connection
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_warning_info
from Subpages.Operational.F3b_operational_functions import input_validation, input_safety_validation, get_order_details, get_company_logo_screen_details, input_validation_order_exists
from Subpages.Services.F3_load_data_from_DB import load_f3_data
from Subpages.SQL.F3b_SQL_queries import sql_query_overview_invoices
from Subpages.SQL.F3_SQL_queries import F3InputDataQueries
from Subpages.Services.F3b_tab3_UI_operations import initiate_session_state_f3b_tab3, reset_filters_f3b_tab3, display_filter_options_f3b_tab3
from Subpages.Services.F3b_tab4_UI_operations import display_filter_options_f3b_tab4, initiate_session_state_f3b_tab4, reset_filters_f3b_tab4
from Subpages.Services.F3b_tab3_execution_logic import execute_f3b_tab3_logic
from Subpages.Services.F3b_tab4_execution_logic import execute_f3b_tab4_logic


# Diagnostics
# import uuid
# import logging
# from app_logging import inicialization_logging
# inicialization_logging()

# if "_debug_session_id" not in st.session_state:
#     st.session_state["_debug_session_id"] = uuid.uuid4().hex[:8]

# run_id = uuid.uuid4().hex[:8]
# logging.warning(
#     f"F3B SCRIPT START | SESSION: {st.session_state['_debug_session_id']} | RUN: {run_id}"
# )

# ================ Application Screen - INPUT Buttons ========================
st.write("# Find your invoice:")
''

st.write("- View into DB. Based on invoices created in Function 3...")
''

tab1, tab2, tab3, tab4 = st.tabs([
    "Last 15 invoices",
    "Search for specific invoice",
    "Customized search",
    "Analytics"
])


# DB engine to be distributed across all tabs
db_engine = db_connection("F3B", True)

# ================= Tab 1 ======================
with tab1:

    ''
    if st.button("Show last 15 offers", width="stretch", icon=UiConfigAndIcons.Buttons.show_table):

        df = pd.read_sql(sql_query_overview_invoices, db_engine)

        # DF styling

        # This makes index + 1 -> by adding new column which is based on index number + 1 (normal df_styled.index = df_styled.index + 1 here doesn't work due to the style. - ing)
        df[" "] = df.index + 1
        df = df.set_index(" ")

        df["Date"] = pd.to_datetime(df["Date"])

        df_styled = df.style.format({
            "Price": "{:,.2f}",
            "Extra service price": "{:,.2f}",
            "Transport price": "{:,.2f}",
            "Total price": "{:,.2f}",
            "Date": lambda d: d.strftime("%d-%b-%Y")
            })
        
        ''
        st.dataframe(df_styled, width = "stretch", height=562)

# ================= Tab 2 ======================

with tab2: 

    with st.form(key="user_form"):
        order_input = st.text_input(label="Order number:", help="Insert **Order number** of invoice you would like to see. It is based on invoices created in **Function 3**.")

        order_input=order_input.strip()
        
        submit_button = st.form_submit_button(label= "Submit", width="stretch", icon=UiConfigAndIcons.Buttons.submit)
    

    if submit_button:          

        # Trigger function 2 only in case that valid and safe input (SQL injestion) and Order number found in DB
        if not input_validation(order_input) or not input_safety_validation(order_input) or not input_validation_order_exists(db_engine, order_input) :
            pass  # pass because of Streamlit script -> to continue with loadign of other TABs


        # Tab 2 main being triggered here
        else:

            result = get_order_details(db_engine, order_input)

            image_company, size = get_company_logo_screen_details(result.transport_company) 

            # ===== UI user screen =====
            ''
            ''
            st.write(f"- Invoice was originally produced in **{result.file_format}** format")
            ''
            st.write("- Invoice overview:")
            st.dataframe(result.df_overview_styled, hide_index=True)

            ''
            st.write("- Product overview:")
            st.dataframe(result.df_product_styled, hide_index=True)

            ''
            st.write("- Extra service overview:")
            st.dataframe(result.df_extra_service_styled, hide_index=True)

            ''
            st.write("- Transport overview:")
            st.image(image_company, width= size)
            st.dataframe(result.df_transport_styled, hide_index=True)

            ''
            if result.df_mapping_empty_bool == True:
                st.write("- Logs - Invoice mapped to differnet format: **no mapping**")
                st.dataframe(result.df_mapping_logs_styled)
            else:
                st.write("- Logs - Invoice mapped to differnet format:")
                st.dataframe(result.df_mapping_logs_styled)  

# =================  Tab 3  ======================

with tab3:

    execution_data: dict = load_f3_data(db_engine, "F3B")

    # Validation
    if execution_data == {} or any(value is None or value == [] for value in execution_data.values()):
        render_warning_info("**Technical issue** - this part is not available.")
        # UI will not render this tab3 and will continue to tab4

    else:
        # Extend by default state conditions
        execution_data["submit_disabled"] = False
        execution_data["checkbox_date"] = False
        execution_data["checkbox_text"] = False
        execution_data["customer_applicable"] = False
        execution_data["product_applicable"] = False
        execution_data["number_rows"] = 20

        initiate_session_state_f3b_tab3(execution_data)   

        selected_data: dict = display_filter_options_f3b_tab3(execution_data)

        ''
        submit_button_tab3 = st.button("Apply filters", width= "stretch", icon=UiConfigAndIcons.Buttons.apply_filters)

        if submit_button_tab3:
            execute_f3b_tab3_logic(
                db_engine,
                selected_data
            )

        # ===== Reset button =====
        st.write("-" *10)
        st.button(
            "Reset filters",
            on_click=reset_filters_f3b_tab3,
            args=(execution_data,),
            width="stretch",
            icon=UiConfigAndIcons.Buttons.reset,
            key="key_reset_button_f3b_tab3"
            )

# =================  Tab 4  ======================

with tab4:

    # Get min date for widget 
    # Put here into main process stream tu avoid calling DB when UI/set of filters (st.fragment) and pass it as parameter
    df_min_date = pd.read_sql_query(sql=text(F3InputDataQueries.sql_query_min_date), con=db_engine)
    min_date = df_min_date["date"].iloc[0]  


    # Extend by default state condition
    execution_data["key_radio_date_f3b_tab4"] = "All invoices - no specific date"

    initiate_session_state_f3b_tab4()

    # UI
    selected: dict = display_filter_options_f3b_tab4(min_date)
    ''
    ''
    submit_button_tab4 = st.button("Apply filters", width= "stretch", icon=UiConfigAndIcons.Buttons.apply_filters, key="key_submit_button_tab4")

    if submit_button_tab4:
        execute_f3b_tab4_logic(db_engine, selected)


    # ===== Reset button =====
    st.write("-" *10)
    st.button(
        "Reset filters",
        on_click=reset_filters_f3b_tab4,
        width="stretch",
        icon=UiConfigAndIcons.Buttons.reset,
        key="key_reset_button_f4b_tab3"
        )