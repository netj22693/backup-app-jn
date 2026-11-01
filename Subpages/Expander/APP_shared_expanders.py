import streamlit as st
from Subpages.Resources_ui import UiConfigAndIcons


def diplay_how_to_use_filters_expander():   

    '''
    - Help to user to navigate throught the buttons and principle
    - Shared expander between F3B TAB3 and F7B TAB3
    - These are sharing the same execution logic
    '''

    with st.expander("How to use the filters", width="stretch", icon=UiConfigAndIcons.Expanders.help_additional_info):
        
        st.write(f"""
        - **Apply filters** {UiConfigAndIcons.Buttons.apply_filters} - Click this button to execute the query using your selected filters. Changes to filters will not take effect until you click it.

        - **Filter persistence** - Your filter selections will be preserved when switching between tabs during the same session.

        - **Reset filters** {UiConfigAndIcons.Buttons.reset} - Click this button to restore all filters to their default values.

        - **Page refresh** :material/refresh: - Refreshing the browser page will also restore the filters to their default values.
        """)