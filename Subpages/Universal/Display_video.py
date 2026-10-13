import streamlit as st
import logging
from app_logging import inicialization_logging

# # ===== Inicialization for logging ===== 
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
        # st.write(path)
        st.video(path)

    except Exception as e:
        logging.warning(f"DESC - display_video(): {path} - FAIL - Exception: {e}")
        st.warning(WARNING)



def display_video_expander(config: dict, list_video: list[str] | None = None):

    '''
    Option 1: creation of expander + load of ALL videos in a logical dictionary group -> list_video = None
    Option 2: creation of expander + load of specific video(s) from a logical dictionary group -> list_video = [] list of key(s)/the specific video(s)   
    '''
   
    if list_video is None:
        videos = list(config.items())
    else:
        videos = []

        for title in list_video:
            if title not in config:
                logging.warning(f"DESC - display_video_expander() - FAIL - Title: '{title}' not on config file")
                continue

            videos.append((title, config[title]))
    
    if len(videos) > 1:
        plural = "s"
    else:
        plural = ""

    with st.expander(f"{EXPANDER_CONFIG['name']}{plural}", icon= EXPANDER_CONFIG["icon"]):

        for title, path in videos:
            st.write(f"**{title}**")
            display_video(path)
            st.write("")