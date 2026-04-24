import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Subpages.FVA_answers import ANSWERS
from Subpages.FVA_questions import FAQ



questions = [item["q"] for item in FAQ]


# --- TF-IDF ---
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)


# --- FUNCTION ID PARSER (FIXED ORDER + SAFE) ---
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


# --- SCORING ---
def score_item(user_input, item, tfidf_score):
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


# --- MAIN LOGIC ---
def get_answer(user_input):
    user_vec = vectorizer.transform([user_input])
    sims = cosine_similarity(user_vec, X)[0]

    best_idx = -1
    best_score = -1e9

    for i, item in enumerate(FAQ):
        score = score_item(user_input, item, sims[i])

        if score > best_score:
            best_score = score
            best_idx = i

    if best_score < 0.3:
        return None

    ans = ANSWERS[FAQ[best_idx]["answer_id"]]
    return ans


# --- STREAMLIT UI ---
st.title("🤖 FAQ Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    answer = get_answer(user_input)

    if answer is None:
        answer = {"text": "Hmm, I don't know this 🤔 Try to rephrase.", "image": None}

    st.session_state.messages.append({"role": "assistant", "content": answer["text"]})

    with st.chat_message("assistant"):
        st.markdown(answer["text"])

        if answer["image"] is not None:
            st.image(answer["image"])