import streamlit as st
import logging
import textwrap
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

    elif page_key == "release_notes":
        label = UiConfigAndIcons.Pages.release_notes["label"]
        page = Assets.Paths.ReleaseNotes.rn
        icon = UiConfigAndIcons.Pages.release_notes["icon"]

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



# =====  st. info message wrappers ===== 

'''
Convention
-----------

Single line info messages:
--------------------------

**<Issue name>** - <Issue description / follow up for user>.

• <Issue name> - Starts with CAPITAL e.g. 'Missing input' text in BOLT
• <Issue description / follow up> - small letters e.g. 'no data in DB'
• (!) The info note should end using dot '.'
• (!) Do not use isn't, doesn't, etc. -> use formal English: is not, does not, etc.


Examples:
1) "**No result** - no data in DB related to the selected date range."
2) "**Missing input** - please provide order number."
3) f"**No result** - order number **{order_input}** does not exist."

Exceptions allowed:
--------------------------
• Keep similar priciple
• Can be adjusted. Key rule is to always have nice and clear user experience.

Fallback display image/video/map:
-----------------------------
• Unable to display the image.
• Unable to display the video.
• Unable to display the map.
'''


# textwrap. is used to have bulletpoints formatted. Simple formatting.

def render_success_info(text:str):
    st.success(
        textwrap.dedent(text).strip(),
        icon=UiConfigAndIcons.InfoText.success,
    )

def render_warning_info(text:str):
    st.warning(
        textwrap.dedent(text).strip(),
        icon=UiConfigAndIcons.InfoText.warning,
    )

def render_error_info(text:str):
    st.error(
        textwrap.dedent(text).strip(),
        icon=UiConfigAndIcons.InfoText.warning,
    )

def render_info_info(text:str):
    st.info(
        textwrap.dedent(text).strip(),
        icon=UiConfigAndIcons.InfoText.info,
    )