# python_faq_chatbot_v5_personality.py
import streamlit as st
import random
import difflib

st.set_page_config(page_title=" Agamemnon — 10-FJK Chatbot", page_icon="🤖", layout="centered")
st.title("Agamemnon — Python Tutor & FAQ")
st.write("Ask me about Python, request a challenge, or say something casual.")

# -----------------------
# Data
# -----------------------
faq = {
    "what is python": "Python is a high-level, interpreted programming language known for readability and versatility.",
    "who created python": "Python was created by Guido van Rossum and first released in 1991.",
}

fun_facts = [
    "Python's name comes from 'Monty Python', not the snake!",
    "You can reverse a string like this: `s[::-1]`.",
]

challenges = [
    {"title": "Sum of Two Numbers", "task": "Ask the user for two numbers and print their sum.", "hint": "Use `input()` and `int()`.", "checker": "sum_checker"},
    {"title": "Even or Odd", "task": "Read a number and print 'even' or 'odd'.", "hint": "Use `% 2` to check remainder.", "checker": "evenodd_checker"},
]

# -----------------------
# Personalities
# -----------------------
personality_modes = ["Friendly", "Formal Tutor", "Funny/Sarcastic"]

# Short-term memory
if "history" not in st.session_state:
    st.session_state.history = []
if "last_challenge" not in st.session_state:
    st.session_state.last_challenge = None
if "personality" not in st.session_state:
    st.session_state.personality = "Friendly"

# -----------------------
# Helpers
# -----------------------
def normalize(text: str) -> str:
    return text.lower().strip()

def find_faq_answer(msg):
    msg = normalize(msg)
    for key in faq:
        if key in msg:
            return faq[key]
    return None

def wants_challenge(msg):
    keywords = ["challenge", "task", "exercise", "problem", "practice"]
    msg = normalize(msg)
    return any(k in msg for k in keywords)

def generate_response(msg):
    msg_norm = normalize(msg)
    # Small talk & facts
    if any(g in msg_norm for g in ["hi", "hello", "hey"]):
        return random.choice(["Hey there!", "Hello!", "Yo! Ready to code?"])
    if "cool" in msg_norm or "fun fact" in msg_norm:
        return random.choice(fun_facts)
    # Challenge
    if wants_challenge(msg_norm):
        ch = random.choice(challenges)
        st.session_state.last_challenge = ch
        return f"🧩 **Challenge - {ch['title']}**\n{ch['task']}\n💡 Hint: {ch['hint']}"
    # FAQ
    faq_answer = find_faq_answer(msg_norm)
    if faq_answer:
        return faq_answer
    # Personality fallback
    return personality_response(msg_norm)

def personality_response(msg):
    mode = st.session_state.personality
    if mode == "Friendly":
        return f"Hey! I'm not sure about that. Try asking about Python, lists, or challenges!"
    elif mode == "Formal Tutor":
        return f"I'm sorry, I do not understand. Please ask a question about Python programming or request a coding challenge."
    elif mode == "Funny/Sarcastic":
        return f"Hmm… I could tell you, but then I'd have to debug your code for you! 😏"
    else:
        return "Hmm… try asking a Python question."

# -----------------------
# Challenge Checkers
# -----------------------
def sum_checker(user_code):
    try:
        local = {}
        exec(user_code, {}, local)
        if "result" in local and local["result"] == 7:
            return True
    except:
        pass
    return False

def evenodd_checker(user_code):
    try:
        local = {}
        exec(user_code, {}, local)
        if "output" in local and local["output"] in ["even", "odd"]:
            return True
    except:
        pass
    return False

# -----------------------
# Streamlit UI
# -----------------------
# Personality mode selector
st.sidebar.selectbox("Personality Mode", personality_modes, key="personality")

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    msg = user_input.strip()
    response = generate_response(msg)
    st.session_state.history.append(("You", msg))
    st.session_state.history.append(("Agamemnon", response))

# Display chat
for speaker, text in st.session_state.history:
    st.markdown(f"**{speaker}:** {text}")

# Interactive challenge submission
if st.session_state.last_challenge:
    st.write(f"Submit code for: **{st.session_state.last_challenge['title']}**")
    user_code = st.text_area("Your Python code here:")
    if st.button("✅ Check Code"):
        checker_name = st.session_state.last_challenge.get("checker")
        if checker_name in globals():
            result = globals()[checker_name](user_code)
            if result:
                st.success("Wow, sakto! 🎉")
            else:
                st.error("Paminaw ni sir dodong/indae!")

# Clear chat
if st.button("Clear Chat"):
    st.session_state.history.clear()
    st.session_state.last_challenge = None
    st.experimental_rerun()
