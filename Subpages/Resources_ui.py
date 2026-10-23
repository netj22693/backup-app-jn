'''
class BaseIcons
- This is just a higher leve of abstraction to re-use icons across widgets in class UiConfigAndIcons
- (!) Do NOT import from this class directly to the code
'''
class BaseIcons:
    pie_chart = ":material/clock_loader_40:"
    code = ":material/code:"
    table = ":material/table:"

    success = ":material/check:"
    warning = ":material/warning:"
    info = ":material/info:"

'''
class UiConfigAndIcons
- For direct import into the code
'''
class UiConfigAndIcons:
    class BusinessIcons:
        # --- These icons are used also in diagrams ---
        # Consider this before changing
        truck = ":material/local_shipping:"
        train = ":material/train:"
        airplane = ":material/travel:"
        # ---------------------------------------------
    
    class InfoText:
        # st.success()
        success = BaseIcons.success
        # st.warning(), st.error()
        warning = BaseIcons.warning
        # st.info()
        info = BaseIcons.info
        
    class Buttons:
        download = ":material/download:"
        close = ":material/close:"
        submit = ":material/apps:"
        reset = ":material/delete:"
        show_table = BaseIcons.table
        show_pie_chart = BaseIcons.pie_chart

        open_new_tab = {
            "icon": ":material/launch:",
            "label": "Open in new tab",
            "help": "Opens in a new tab."
        }

    class Toasts:
        success = BaseIcons.success
        warning = BaseIcons.warning

        # Time to keep the toast visible - duration in seconds
        duration = {
            "standard_notification" : 10, # Standard short notification
            "important_notification" : 25  # Function execution context
        }

    class Expanders:
        help_additional_info = ":material/help_outline:"
        code_structure = BaseIcons.code
        table = BaseIcons.table
        pie_chart = BaseIcons.pie_chart
        bar_chart = ":material/bar_chart:"
        limitation = ":material/sync_problem:"
        map = ":material/pin_drop:"
        list = ":material/list:"
        video = ":material/youtube_activity:"
        # Used in F7 desc Metrics - description of measuring method of distance
        measurment = ":material/square_foot:"
        # Used in F7 transport flow
        state_flow = ":material/line_end_circle:" 

    class Pages:

        # Navigation through the app 
        help_text = "Go to the relevant page."

        # CButtons config
        width = "stretch"


        landing_page = {
            "icon": ":material/home:",
            "label": "Home page"
        }

        architecture = {
            "icon": ":material/architecture:",
            "label": "Application Architecture"
        }

        virtual_assistant = {
            "icon": ":material/smart_toy:",
            "label": "Virtual Assistant (Chatbot)"
        }

        bug_form = {
            "icon": ":material/pest_control:",
            "label": "Have you seen a bug?"
        }

        release_notes = {
            "icon": ":material/event_note:",
            "label": "Release notes"
        }

        description = {
            "icon": BaseIcons.code,
            # label - not possible to make generic -> Description X
        }
        function = {
            "icon": ":material/play_circle:",
            # label - not possible to make generic -> Function X
        }

        next_page = {
            "icon": ":material/east:",
            "label": "Next page"
        }

        previous_page = {
            "icon": ":material/west:",
            "label": "Previous page"
        }