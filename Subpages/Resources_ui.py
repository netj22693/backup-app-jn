class UiConfigAndIcons:
    class BusinessIcons:
        # --- These icons are used also in diagrams ---
        # Consider this before changing
        truck = ":material/local_shipping:"
        train = ":material/train:"
        airplane = ":material/travel:"
        # ---------------------------------------------

    class Buttons:
        download = ":material/download:"
        close = ":material/close:"
        submit = ":material/apps:"
        reset = ":material/delete:"
        show_table = ":material/table:"
        show_pie_chart = ":material/clock_loader_40:"

        open_new_tab = {
            "icon": ":material/launch:",
            "label": "Open in new tab",
            "help": "Opens in a new tab."
        }

    class Toasts:
        success = ":material/check:"
        warning = ":material/warning:"

        # Time to keep the toast visible - duration in seconds
        duration = {
            "standard_notification" : 10, # Standard short notification
            "important_notification" : 25  # Function execution context
        }

    class Expanders:
        help_additional_info = ":material/help_outline:"
        code_structure = ":material/code:"
        table = ":material/table:"
        pie_chart = ":material/clock_loader_40:"
        bar_chart = ":material/bar_chart:"
        limitation = ":material/sync_problem:"
        map = ":material/pin_drop:"
        list = ":material/list:"
        # Used in F7 desc Metrics - description of measuring method of distance
        measurment = ":material/square_foot:"
        # Used in F7 transport flow
        state_flow = ":material/line_end_circle:" 

    class Pages:

        # Navigation throught the app 
        help_text = "Go to the relevant page."

        # Config for buttonts
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

        description = {
            "icon": ":material/code:",
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
