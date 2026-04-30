from Subpages.Resources import Assets
from Subpages.Resources import HELLO_STATEMENT


ANSWERS = {
#  ======= General answers =======
"va_hi_hello": {
    "text": f"{HELLO_STATEMENT}",
    "image": None
},

"va_name": {
    "text": "I do not have specific name, I am just your virtual assistant :blush:",
    "image": None
},

"va_age": {
"text": """I was born in **April 2026**. Within **v60.2** version of the application :innocent::fire:.\n\n
If you are interested in releases, go to main page :house:-> Expander: **Release notes** :green_heart:
""",
"image": None
},

"va_mood": {
    "text": "I am doing good :blush::smirk::green_heart:",
    "image": None
},

"va_principle": {
"text": f"""The chatbot works on the following principle:\n\n
- **Simply**: The bot mathematically finds the most similar predefined question and returns the corresponding prepared response.\n\n
- **Detailed**:penguin::
    - User enters a question
    - The bot takes all FAQ questions (predefined in the code as dictionary)
    - Text is split into words and converts questions into numerical vectors - :blue[**TfidfVectorizer()**]
    - The user input is transformed into a vector using the same logic
    - Similarity between the user question and all FAQ questions - :blue[**cosine_similarity()**]
    - Additional custom scoring is applied using (In dictionary):
        - keywords
        - tags
        - function_id
    - The FAQ item with the highest final score is selected
    - Responses can contain:
        - text
        - images
        - links\n\n

- :rocket: **LLM** - currently there is **no** LLM behind. The bot use uses only mathematical principle based on functions from sklearn / Scikit-Learn [here]({Assets.Links.sklearn_library}) :point_left:.
""",
"image": Assets.Images.va_variables
},

"llm_principle": {
"text": f""":rocket: **LLM** - currently there is **no** LLM behind. The bot use uses only mathematical principle based on functions from sklearn / Scikit-Learn [here]({Assets.Links.sklearn_library}) :point_left:.
""",
"image": None
},


"overview": {
"text": """The application has **multiple functions inspired by real business use-cases**. It uses:
- **REST APIs** 
- **PostgreSQL DB**
- Principle of standard CRUD operations (specifically **C**reate and **R**ead)""",
"image": Assets.Images.architecture_landscape
},


"overview_principle": {
"text": "The application has multiple functions inspired by real business use-cases.",
"image": None
},


"functions_count": {
"text": """There are 8 functions currently.
- **Function 1:** Download of few predefined types of XML for Function 2
- **Function 2:** Parsing of data from XML -> their visualization -> producing of simple .txt file as summary      
- **Function 3:** Creation of XML (slightly different one than used in F1 and F2) or JSON, through the application screen (manual inputs) - **DB on cloud**
- **Function 4:** Mapping/change of file format XML -> JSON or JSON -> XML 
- **Function 5:** Exchange rate/calculation (CZK, EUR, USD) - **API based** with actual exchange rate
- **Function 6:** ZIP code - (1) Get ZIP code(s) based on City, (2) Get City based on ZIP code - **API based**
- **Function 7:** Transport calculation - **API** provides input & **DB on cloud** (:green[**my favorit function**])
- **Function 8:** Company Book - provides visibility of transport companies - **DB on cloud** """,
    "image": None
},


"generic_APIs": {
    "text": "There are 7 REST APIs used in the application. See architecture diagram below.",
    "image": Assets.Images.architecture_landscape
},

"db_info": {
"text": f"""Information about DB:
- The application uses **PostgreSQL DB** which runs on **NEON DB cloud**.
- The relations **READ/WRITE** per functions can be seen in **the Archimate diagram**.\n\n
👉 You can find more details about DB structures:
- **Functions 3 & 4**: [here]({Assets.Links.f3_f4_description_erd})
- **Function 7 & 7B**: [here]({Assets.Links.f7_description_erd})
- **Function 8**: [here]({Assets.Links.f8_descriptin_erd})
""",
"image": Assets.Images.archimate_main
},


"more_details": {
"text": """Each function has subpages called **Description** providing more details/info:

- How the functions work 
- What is the technical & business inside/logic\n\n

It is described not only by text but also by modeling languages like **BPMN, Archimate, UML**.\n\n
:point_left: The subpages can be seen in the navigation bar on the left.
""",
"image": None
},


"example_questions": {
"text": f"""You can ask me and I will answer and explain:\n\n
Questions **about me (chatbot**), for example:
- How do you work?
- How old the chatbot is?

\n\n
Or **generic questions about the application**, for example:
- What does the application do?
- How does the application work?
- Where can I get more info/details about the functions?
- When the application was released?
- For how long it has been built?
- ...
\n\n

Or **questions related to specific functions**:
- What does Function 1 do?
- How does the Function 1 work?
- ...

**Tip:** You can also use just simple F and number of function you are interested in -> **F7** :relaxed:
""",
"image": None
},


"build_app": {
"text": f"""
- The application has been built since **February 2025**. 
- It started as a small project for fun 
- Function 1 and Function 2 were first and released together 
- More details can be see on the main page :house: - Expander: **Release notes** :green_heart:
""",
"image": None
},

"author" : {
"text": f"""
- The application was built by Jan Netolicka. :wave::v:
- LinkedIn profile [Here]({Assets.Links.linked_in}) :panda_face:
""",
"image": None
},

#  ---- What is question ----
"what_is_xml" : {
"text": f"""
**Extensible Markup Language (XML)** is a markup language and file format for storing, transmitting, and reconstructing data. It defines a set of rules for encoding documents in a format that is both human-readable and machine-readable. 

👉 You can find more details how XML is used in this application:
- **Functions 1 & 2**: [here]({Assets.Links.f2_xml_xsd})
- **Function 3**: [here]({Assets.Links.f3_f4_xml_xsd})
""",
"image": None
},

# XSD - used by F2 and F3
"what_is_xsd": {
"text": f"""**XSD** or also known as **XML Schema is:**
- .xsd file which describes rules of XML file
- XSD is basically template based on which you can compare, if XML file follows all requirements it should have - defined structure, defined data and their types
- **If XML is not fully in line with XSD, there is a fallback logic. Reason: it prevents code from crashing. :ok_hand:**

👉 You can find more details:
- **Function 1 & 2**: [here]({Assets.Links.f2_xml_xsd}) 
- **Function 2 - XML against XSD validation**: [here]({Assets.Links.f2_xml_xsd_validation})
- **Function 3**: [here]({Assets.Links.f3_f4_xml_xsd})
""",
"image": Assets.Images.f2_xml_xsd_validation
},

"what_is_json" : {
"text": f"""
**JSON (JavaScript Object Notation)** is a lightweight, text-based data-interchange format used to store and transport data, often between a server and a web application. It is language-independent, human-readable, and based on **key/value pairs**. It is widely used in **API outputs**, configuration files, and AJAX, serving as a faster, modern alternative to XML. 

👉 You can find more details how JSON is used in this application:
- **Function 3 and 4**: [here]({Assets.Links.f3_f4_json}) - building our own JSON
- **Function 5**: [here]({Assets.Links.f5_description}) - JSON used in API from external system
- **Function 6**: [here]({Assets.Links.f6_description}) - JSON used in API from external system
""",
"image": None
},


#  ======= Function related answers =======
#  ---- Function 1 ----
"function_1": {
"text": """**Function 1** (Download xml) **supports Function 2** (Parsing, Validation, Visualization)
- You can download some of **predefined XML files** or **create your own** following XML template. 
- There is **also possibility to download XSD / XML Schema** so you **can check that your XML is correct** before upload to Function 2.""",
"image": Assets.Images.uml_f1_f2
},
"function_1_insight" : {
"text": "**Function 1** works on simple principle of download button which downloads selected XML file to user's device (usually Downloads folder). That's it. :wink:",
"image": None
},

#  ---- Function 2 ----
"function_2": {
"text": "**Function 2** (Parsing, Validation, Visualization) - Upload XML, parse and visualize data.",
"image": Assets.Images.uml_f1_f2
},

"function_2_insight": {
"text": """**Function 2** works on **5 steps** principle:

- **Step 1** - User uploads XML file  
- **Step 2** - Data are validated against XSD  
- **Step 3** - Data are parsed from XML  
- **Step 4** - Data are visualized in tables and charts  
- **Step 5** - User can download summary (.txt)
""",
"image": None
},

"function_2_xml" : {
"text": f"""**XML** for **Function 2** can be donwloaded from **Function 1**.\n\n

👉 **Funtion 1**: [here]({Assets.Links.f1_function})
""",
"image": None
},

#  ---- Function 3 ----
"function_3": {
"text": "**Function 3**: Creation of invoice based on user inputs (either XML or JSON). Possibility to create your own invoice based on predefined options. Fulfill the UI form and select if to generate XML or JSON. The final data are stored in DB",
"image": Assets.Images.uml_f3_f3b_f4
},
"function_3B": {
"text": "**Function 3B**: Visibility of already created invoices. Insight into DB to see already created invoices from Function 3.",
"image": Assets.Images.uml_f3_f3b_f4
},
"function_4" : {
"text": f"""**Function 4**: Mapping of invoice from Function 3 -> change of file format.\n\n
- XML → JSON 
- or JSON → XML\n\n
There is a log about the change stored in DB.\n\n
More details can be found in the function description [here]({Assets.Links.f3_description}) :point_left:""",
"image": Assets.Images.uml_f3_f3b_f4
},
"function_5" : {
"text": f"""**Function 5:** Exchange rate/calculation (CZK, EUR, USD).\n\n
- It is a simple calculator which uses actual conversion rate 
- There are 2 open APIs from external systems providing the conversion rate\n\n
More details can be found in the function description [here]({Assets.Links.f5_description}) :point_left:
""",
"image": Assets.Images.uml_f5
},
"function_6" : {
"text": f"""**Function 6:** ZIP codes. You can search for:\n\n
- ZIP codes based on city
- or city based on ZIP codes\n\n
The function uses 2 APIs as a source of data.\n\n
More details can be found in the function description [here]({Assets.Links.f5_description}) :point_left:""",
"image": Assets.Images.uml_f6
},
"function_7" : {
"text": f"""**Function 7:** Transport calculation:\n\n
- **The biggest** function in this application
- **Configurator and calculator** of transport cost, journey distance and lasting of the delivery based on:
    - Transport type (Truck, Train, Airplane)
    - Distance of journey
    - Delivery service (Express, Standard, Slow)
    - Door-to-Door delivery or not - more details about DTD on the next page
    - Shipment specifications (Insurance extra, Danger or Fragile goods
- Uses API as source of data - actual exchange rate\n\n
- Outcome of this function is **PDF file (Offer)** and the **data are saved into DB**.

More details can be found in the function description [here]({Assets.Links.f7_description}) :point_left:
""",
"image": Assets.Images.uml_f7_f7b
},
"function_7B" : {
"text": f"""**Function 7B**: View into DB. Based on offers created in Function 7
- The 7B uses data created in Function 7
- There is multiple tabs allowing to search and filter in the already created offers
- The data also allows to make an analytic stuff/data visualization using tables and charts\n\n
The data is taken from database. More details about the **DB structure** can be found in the description here [here]({Assets.Links.f7_description_erd}) :point_left:

""",
"image": Assets.Images.uml_f7_f7b
},
"function_8" : {
"text": f"""**Function 8**: Company Book - provides visibility of transport companies and their branches.\n\n
- The transport companies are companies from real world
- The data in DB are collected from the internet
- Multiple tabs allowing different point of views on the data 
- Source of data is DB running on cloud\n\n

More details can be found in the function description [here]({Assets.Links.f8_description}) :point_left:
""",
"image": Assets.Images.uml_f8
},
}