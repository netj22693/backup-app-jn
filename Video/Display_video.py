import streamlit as st
import logging
from app_logging import inicialization_logging
from Subpages.Resources_ui import UiConfigAndIcons
from Subpages.Resources_ui_objects import render_warning_info


# ===== Inicialization for logging ===== 
inicialization_logging()

# ===== Config file ===== 
EXPANDER_CONFIG = {
    "name": "Video guide",
    "icon": UiConfigAndIcons.Expanders.video,
    "warning": "Unable to display the video.",
    "caption_outdated": f"{UiConfigAndIcons.InfoText.warning} This video may be outdated. Some features may have changed or may not be shown."
    }


def display_video(path: str | None, outdated: bool | None):

    if path is None:
        logging.warning(f"DESC - display_video() - FAIL - Not existing key")
        render_warning_info(EXPANDER_CONFIG["warning"])
        return

    try:
        if outdated:
            st.caption(EXPANDER_CONFIG["caption_outdated"])
        st.video(path)

    except Exception as e:
        logging.warning(f"DESC - display_video(): {path} - FAIL - Exception: {e}")
        render_warning_info(EXPANDER_CONFIG["warning"])


def display_video_expander(config: dict, list_video_include: list[str] | None = None, list_video_exclude: list[str] | None = None):

    '''
    - Creation of expander rendering & load of videos
    - 'config' is logical group of videos
    - 'config' dict structure principle {"video_title": "video_path"}
    - Possibility to use either include or exclude approach to manage what should/shoudn't be visible

    Note:
    - The function follows order based on data provided (config) -> if specific order of videos required, use list_video_include[] to explicitly define the order in which videos should be displayed
    '''

    # Below there can be DEL operation -> to do not rewrite the existing dict -> copy created
    config = config.copy()

    if list_video_include is not None and list_video_exclude is not None:
        logging.warning(f"DESC - display_video_expander() - FAIL - Both Include and Exclude lists provided")
        return
   
    elif list_video_exclude is not None:

        if len(list_video_exclude) == 0:
            logging.warning(f"DESC - display_video_expander(): Exclude - FAIL - Empty list")
            return

        for title in list_video_exclude:
            if title not in config:
                logging.warning(f"DESC - display_video_expander(): Exclude - FAIL - Title: '{title}' not on config file")
                continue

            else:
                del config[title]
                continue

        videos = list(config.items())

    elif list_video_include is not None:

        if len(list_video_include) == 0:
            logging.warning(f"DESC - display_video_expander(): Include - FAIL - Empty list")
            return

        
        videos = []

        for title in list_video_include:
            if title not in config:
                logging.warning(f"DESC - display_video_expander(): Include - FAIL - Title: '{title}' not on config file")
                continue

            videos.append((title, config[title]))

    else:
        videos = list(config.items())


    if len(videos) == 0:
        logging.warning(f"DESC - display_video_expander() - FAIL - Empty list []")
        return


    if len(videos) > 1:
        plural = "s"
    else:
        plural = ""


    with st.expander(f"{EXPANDER_CONFIG['name']}{plural}", icon= EXPANDER_CONFIG["icon"]):
       
        for title, video_config in videos:
            try:
                path = video_config["path"]
                outdated = video_config["outdated"]

                st.write(f"**{title}**")
                display_video(path, outdated)
                st.write("")

            except KeyError:
                logging.warning(f"DESC - display_video_expander() - FAIL - KeyError for title: {title}")

            except Exception as e:
                logging.warning(f"DESC - display_video_expander() - FAIL - Exception: {e} for title {title}")
