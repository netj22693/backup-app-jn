# Purpose: UI for F3 and F3B TAB3 has the same config input
# Centralization of the different parts of the Function 3

'''
F3_ICONS 1 CONFIG_WIDGETS
- Higher level of abstraction to re-use icons across widgets in CONFIG_UI_INPUTS
- (!) Do NOT import from these directly to the code
'''
F3_ICONS = {
    "customer": ":material/tag_faces:",
    "product": ":material/devices:",
    "currency": ":material/euro_symbol:",
    "additional_service": ":material/exposure_plus_1:",
    "icon_transport": ":material/directions_bus:",
    "icon_parcel": ":material/box:",
    "icon_pin": ":material/pin_drop:",
    "file_format": ":material/draft:"
}


CONFIG_WIDGETS = {
    "placeholders_widgets": {
        "text": "Type...",
        "select": "Select...",
    },
    "placeholder_help":{
        "select": "Select one from the options."
    },
    "limits": {
        "text": 35
    }
}


'''
For direct import into the code
'''
CONFIG_UI_INPUTS = {
    "customer":{
        "name": "Customer/Company name:",
        "icon": F3_ICONS['customer'],
        "help_f3": "Type a customer or company name.",
        "help_f3b": "Search is case-insensitive and matches text anywhere within the value.",
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['text'],
        "limit": CONFIG_WIDGETS['limits']['text'],
    },
    # -----------------------------------------------------------
    "category":{
        "name": "Category:",
        "icon": F3_ICONS['product'],
        "help_f3": CONFIG_WIDGETS['placeholder_help']['select'],
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['select']

    },
    "product":{
        "name": "Product name:",
        "icon": F3_ICONS['product'],
        "help_f3": "Type a product name.",
        "help_f3b": "Search is case-insensitive and matches text anywhere within the value.",
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['text'],
        "limit": CONFIG_WIDGETS['limits']['text']
    },
    # -----------------------------------------------------------
    "currency":{
        "name": "Currency:",
        "icon": F3_ICONS['currency'],
        "help_f3": CONFIG_WIDGETS['placeholder_help']['select'],
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['select'],
    },
    "product_price":{
        "name": "Product price:",
        "icon": F3_ICONS['currency'],
        "help_f3": "You can either click on the +- icons or type the number input.",
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['select'],
    },
    # -----------------------------------------------------------
    "additional_service":{
        "name": "Additional service:",
        "icon": F3_ICONS['additional_service'],
        "help_f3": CONFIG_WIDGETS['placeholder_help']['select'],
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['select'],
    },
    # -----------------------------------------------------------
    "country": {
        "name": "Country:",
        "icon": F3_ICONS['icon_pin'],
        "help_f3": f"{CONFIG_WIDGETS['placeholder_help']['select']} - there is different price for service for each country -> see the pricing table below.",
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['select']
    },
    "transport_company": {
        "name": "Transport company:",
        "icon": F3_ICONS['icon_transport'],
        "help_f3": f"{CONFIG_WIDGETS['placeholder_help']['select']} - there is different price for each company -> see the pricing table below.",
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['select']
    },
    "parcel_size": {
        "name": "Parcel size:",
        "icon": F3_ICONS['icon_parcel'],
        "help_f3": CONFIG_WIDGETS['placeholder_help']['select'],
        "placeholder": CONFIG_WIDGETS['placeholders_widgets']['select']
    },
    # - only in F3B ----------------------------------------------
    "file_format": {
        "name": "File format:",
        "icon": F3_ICONS['file_format']
    }
}