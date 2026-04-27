import streamlit as st
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Subpages.FVA_answers import ANSWERS
from Subpages.FVA_questions import FAQ
from Subpages.Resources import HELLO_STATEMENT



questions = [item["q"] for item in FAQ]

# This part takes the question placed into the chat as sentense and breaks each word into number - TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)


# This part helps to get proper results related to specific functions
# !!!! Note from troubleshooting: for functions having 'B' the 'B' version needs to be in the code upper than 'regular' version. E.g.: 7B followed by 7. If not, then it will nto work properly.
def extract_function_id(text):
    text = text.lower().replace(" ", "")

    if "function8" in text or "f8" in text:
        return "8"

    if "function7b" in text or "f7b" in text:
        return "7B"

    if "function7" in text or "f7" in text:
        return "7"

    if "function6" in text or "f6" in text:
        return "6"

    if "function5" in text or "f5" in text:
        return "5"

    if "function4" in text or "f4" in text:
        return "4"

    if "function3b" in text or "f3b" in text:
        return "3B"

    if "function3" in text or "f3" in text:
        return "3"

    if "function2" in text or "f2" in text:
        return "2"

    if "function1" in text or "f1" in text:
        return "1"

    return None


# Score - taken from sklearn documentation 
def get_score(user_input, item, tfidf_score):
    user_input_lower = user_input.lower()

    keyword_score = sum(
        1 for k in item.get("keywords", [])
        if k.lower() in user_input_lower
    )

    tag_score = sum(
        1 for t in item.get("tags", [])
        if t.lower() in user_input_lower
    )

    user_fn = extract_function_id(user_input)

    fn_score = 0
    if user_fn:
        if item.get("function_id") == user_fn:
            fn_score = 3.0
        else:
            fn_score = -2.0

    return (
        tfidf_score * 0.4 +
        keyword_score * 0.2 +
        tag_score * 0.2 +
        fn_score
    )


# The main logic - taken from sklearn documentation 
def get_answer(user_input):
    user_vec = vectorizer.transform([user_input])
    sims = cosine_similarity(user_vec, X)[0]

    best_idx = -1
    best_score = -1e9

    for i, item in enumerate(FAQ):
        score = get_score(user_input, item, sims[i])

        if score > best_score:
            best_score = score
            best_idx = i

    if best_score < 0.3:
        return None

    ans = ANSWERS[FAQ[best_idx]["answer_id"]]
    return ans

# For Streamlit session state purposes
# Note: in the current version of the code it is not that important, I wanted to have this to call this function also when 'Reset chat' button used. But current streamlit version is having the UI quite locked and the button is appearing in the chat -> Waiting for fix of this on Streamlit side.
def get_welcome_message():

    message = [{
            "role": "assistant",
            "content": HELLO_STATEMENT
        }]
    
    return message


# application UI
st.title("🤖 FAQ Chatbot")

if "messages" not in st.session_state:
    with st.spinner("Loading..."):
        time.sleep(2)
        st.session_state.messages = get_welcome_message()


# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):

        if msg.get("type", "text") == "text":
            st.markdown(msg["content"])

        # In case that there is also image in the selected response
        elif msg.get("type") == "image":
            st.image(msg["content"])


# User input 
user_input = st.chat_input("Ask your question...")

if user_input:
    # User - Streamlit to keep session states and what the UI shouls show on the screen
    st.session_state.messages.append({
        "role": "user",
        "type": "text",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call the main logic 
    answer = get_answer(user_input)

    if answer is None:
        answer = {
            "text": "Hmm, I don't know this 🤔 Try to rephrase.",
            "image": None
        }

    # Assistant (official streamlit term) - Streamlit to keep session states and what the UI shouls show on the screen
    st.session_state.messages.append({
        "role": "assistant",
        "type": "text",
        "content": answer["text"]
    })

    with st.chat_message("assistant"):
        st.markdown(answer["text"])

    # Assistant (official streamlit term) - in case that there is also image in selected response
    if answer["image"] is not None:

        st.session_state.messages.append({
            "role": "assistant",
            "type": "image",
            "content": answer["image"]
        })

        with st.chat_message("assistant"):
            st.image(answer["image"])

# In the current version of streamlit the button cannot be put under the chat bar
# if st.button("Clear chat", width= "stretch", icon= ":material/delete:"):
#     st.session_state.messages = get_welcome_message()
#     st.rerun()

