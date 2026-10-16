import streamlit as st
import logging
from app_logging import inicialization_logging
from Subpages.Resources import Assets
from Subpages.Resources_ui import UiConfigAndIcons

# ===== Inicialization for logging ===== 
inicialization_logging()


# =====  Objects using st.page_link ===== 
def render_next_page(page: str):

    st.page_link(
        label=UiConfigAndIcons.Pages.next_page["label"],
        page=page,
        width=UiConfigAndIcons.Pages.width,
        icon=UiConfigAndIcons.Pages.next_page["icon"]
        ) 


def render_previous_page(page: str):

    st.page_link(
        label=UiConfigAndIcons.Pages.previous_page["label"],
        page=page,
        width=UiConfigAndIcons.Pages.width,
        icon=UiConfigAndIcons.Pages.previous_page["icon"],
        ) 

def render_function_page(label: str, page: str):

    st.page_link(
        label=label,
        page=page,
        width=UiConfigAndIcons.Pages.width,
        icon=UiConfigAndIcons.Pages.function["icon"],
        ) 

def render_description_page(label: str, page: str):

    st.page_link(
        label=label,
        page=page,
        width=UiConfigAndIcons.Pages.width,
        icon=UiConfigAndIcons.Pages.description["icon"],
        ) 

def render_specific_page(page_key: str, label_customized: str | None = None):

    '''
    label: str | None = None in case that the label should be different than standardized


    Links to: 
    - Home page
    - Bug Form
    - Virtual Assistant
    - App Architecture
    '''

    if page_key == "home_page":
        label = UiConfigAndIcons.Pages.landing_page["label"]
        page = Assets.Paths.App.main_page
        icon = UiConfigAndIcons.Pages.landing_page["icon"]

    elif page_key == "bug_form":
        label = UiConfigAndIcons.Pages.bug_form["label"]
        page = Assets.Paths.BugForm.bf
        icon = UiConfigAndIcons.Pages.bug_form["icon"]

    elif page_key == "virtual_assistant":
        label = UiConfigAndIcons.Pages.virtual_assistant["label"]
        page = Assets.Paths.VirtualAssistant.va
        icon = UiConfigAndIcons.Pages.virtual_assistant["icon"]

    elif page_key == "app_architecture":
        label = UiConfigAndIcons.Pages.architecture["label"]
        page = Assets.Paths.App.app_architecture
        icon = UiConfigAndIcons.Pages.architecture["icon"]

    else:
        logging.warning(f"Page rendering - FAIL - Not existing page_key: {page_key}")
        return

    # To use not standardized one
    if label_customized is not None:
        label = label_customized
    
    st.page_link(
        label=label,
        page=page,
        width=UiConfigAndIcons.Pages.width,
        icon=icon,
    ) 

# =====  Objects using st.link_button ===== 

def render_link_button(label: str, url: str):

    st.link_button(
        label=f"Open: {label}",
        url=url,
        help=UiConfigAndIcons.Buttons.open_new_tab["help"],
        width=UiConfigAndIcons.Pages.width,
        icon=UiConfigAndIcons.Buttons.open_new_tab["icon"]
        )