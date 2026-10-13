import streamlit as st
import logging
from app_logging import inicialization_logging


# ===== Inicialization for logging ===== 
inicialization_logging()



EXPANDER_CONFIG = {
    "name": "Video guide",
    "icon": ":material/youtube_activity:"
    }


def display_video(path: str | None):

    WARNING = "Not able to display the video."

    if path is None:
        logging.warning(f"DESC - display_video() - FAIL - Not existing key")
        st.warning(WARNING)
        return

    try:
        st.video(path)

    except Exception as e:
        logging.warning(f"DESC - display_video(): {path} - FAIL - Exception: {e}")
        st.warning(WARNING)



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
        for title, path in videos:
            st.write(f"**{title}**")
            display_video(path)
            st.write("") 