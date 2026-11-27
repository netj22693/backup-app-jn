import streamlit as st
import pandas as pd
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_warning_info
from Subpages.Dialog.APP_universal_dialog import display_download_complete_toast
from Subpages.Operational.F2_operational_functions import df_styling
from Subpages.Universal.Charts import create_pie_chart, create_bar_chart
from Subpages.Universal.Universal_functions import display_df_index_hidden



def initiate_session_state_f2():

    '''
    - The session state is used for having possibility to completelly clear the F2 when Close X button used
    - The session is reset by += 1 in the close_function_f2() triggered as on_click parameter in the close button
    '''

    if "uploader_key_f2" not in st.session_state:
        st.session_state.uploader_key_f2 = 0


def multiselect_validation(values: list, text: str):
        if len(values) == 0:
            render_warning_info(f"At least 1 {text} needs to be selected.")


# ====== Main filtering logic Multiselects, Sliders, dynamic DF =======

@st.fragment()
def display_interactive_table_and_charts(df:pd.DataFrame) -> pd.DataFrame:

    '''
    - Uses @st.fragment
    - UI Function with widgets (2 multiselect + 2 sliders)
    - Dynamic DF based on teh filtering
    - Dysplaing charts
    '''

    category_options = sorted(df["Category"].dropna().unique().tolist())

    additional_services_options = sorted(df['Additional service'].dropna().unique().tolist())


    # Multiselect filter - Category
    st.write("")

    category = st.multiselect(
        "Category",
        category_options,
        default = category_options
    )  

    multiselect_validation(category, "category")

    min_price = df['Price'].min()
    max_price = df['Price'].max()

 
    # Slider - price 
    st.write("")

    from_price, to_price = st.slider(
        "Product price",
        min_value = min_price,
        max_value = max_price,
        value = [min_price, max_price],
        step = 1.00
    )

    # Multiselect filter
    st.write("")
    st.write("")

    additional_services = st.multiselect(
        "Service",
        additional_services_options,
        default = additional_services_options
        )

    multiselect_validation(additional_services,"service") 


    # Slider
    min_price_ads = df["Additional service price"].min()
    max_price_ads = df["Additional service price"].max()
    
    st.write("")

    from_price_ads, to_price_ads = st.slider(
        "Service price",
        min_value = min_price_ads,
        max_value = max_price_ads,
        value= [min_price_ads, max_price_ads],
        step = 1.00
    ) 


    df_filtered = df[
        (df["Category"].isin(category))
        & ((df["Price"] <= to_price) & (df["Price"] >= from_price))
        & (df["Additional service"].isin(additional_services))
        & ((df["Additional service price"] <= to_price_ads) & (df["Additional service price"] >= from_price_ads))
    ]
        

    # DF styling prior data visualization
    df_filtered_styled = df_styling(df_filtered)

    # ===== UI =====
    st.write("")
    st.write("")

    icon_t = UiConfigAndIcons.UnifiedIcons.table
    icon_p = UiConfigAndIcons.UnifiedIcons.pie_chart
    icon_b = UiConfigAndIcons.UnifiedIcons.bar_chart

    tab1, tab2, tab3 = st.tabs([
        f"{icon_t} Overview",
        f"{icon_p} Ratio - Product price",
        f"{icon_b} Product price"
    ])

    with tab1:
        display_df_index_hidden(df_filtered_styled)

    if not df_filtered.empty:    
        with tab2:
            st.plotly_chart(
                create_pie_chart(
                    df_filtered,
                    "Product",
                    "Price",
                    False
                    )
                )
    
        with tab3:
            st.plotly_chart(
                create_bar_chart(
                    df_filtered,
                    "Product",
                    "Price",
                    )
                )


@st.fragment
def download_summary(data: str, file_name: str):
    st.write("#### Summary:")
    st.write("Short summary of the XML invoice, including result of the validation.")

    st.image("Pictures/Function_2/F2_txt_oveview_v2.svg")

    st.write("")
    st.write("")
    st.write("")

    if st.download_button(
        "Download",
        data=data,
        file_name= file_name,
        icon= UiConfigAndIcons.Buttons.download,
        width="stretch"
        ):
            
        display_download_complete_toast()