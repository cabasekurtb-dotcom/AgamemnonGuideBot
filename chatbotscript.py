# python_faq_chatbot_v4_interactive.py
import streamlit as st
import random
import difflib

st.set_page_config(page_title="🐍 Agamemnon — Python Tutor & FAQ", page_icon="🤖", layout="centered")
st.title("🤖 Agamemnon — Python Tutor & FAQ")
st.write("Ask me about Python, request a challenge, or say something casual. (Try: 'Give me a challenge', 'What is a list?', 'Tell me something cool about Python')")

# -----------------------
# Data
# -----------------------
faq = {
    "what is python": "Python is a high-level, interpreted programming language known for readability and versatility. It's used in web development, data science, automation, and more.",
    "who created python": "Python was created by Guido van Rossum and first released in 1991.",
    "what are variables": "Variables store data. Example: `x = 5` or `name = 'Isko'`.",
    "what are data types": "Common types: int, float, str, bool, list, tuple, dict, set. Each stores different kinds of values.",
    "what is a list": "A list is an ordered, changeable collection. Example: `fruits = ['apple','banana']`.",
    "what is a tuple": "A tuple is like a list but immutable. Example: `coords = (10, 20)`.",
    "what is a dictionary": "A dictionary stores key:value pairs. Example: `p = {'name':'Isko','age':15}`.",
}

fun_facts = [
    "Python's name comes from 'Monty Python' — the comedy group, not the snake.",
    "You can reverse a string in Python with slicing: `s[::-1]`.",
]

challenges = [
    {"title": "Sum of Two Numbers", "task": "Ask the user for two numbers and print their sum.", "hint": "Use `input()` and convert to int: `int(input())`.", "checker": "sum_checker"},
    {"title": "Even or Odd", "task": "Read a number and print whether it's even or odd.", "hint": "Use `% 2` to check remainder.", "checker": "evenodd_checker"},
]

casual_responses = {
    "hi": ["Hey!", "Hello!", "Yo! Ready to code?"],
    "thanks": ["You're welcome!", "No problem!"],
    "cool": fun_facts,
}

# -----------------------
# Memory initialization
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "last_topic" not in st.session_state:
    st.session_state.last_topic = None

if "last_challenge" not in st.session_state:
    st.session_state.last_challenge = None

# -----------------------
# Matching helpers
# -----------------------
def normalize(text: str) -> str:
    return text.lower().strip()

def find_faq_answer(msg):
    msg = normalize(msg)
    for key in faq:
        if key in msg:
            st.session_state.last_topic = key
            return faq[key]
    return None

def wants_challenge(msg):
    keywords = ["challenge", "task", "exercise", "problem", "practice"]
    msg = normalize(msg)
    return any(k in msg for k in keywords)

def small_talk_response(msg):
    msg = normalize(msg)
    for k, v in casual_responses.items():
        if k in msg:
            return random.choice(v)
    return None

# -----------------------
# Challenge checkers
# -----------------------
def sum_checker(user_code):
    try:
        # Run code and check result
        local = {}
        exec(user_code, {}, local)
        if "result" in local and local["result"] == 7:  # example: 3+4
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
# Streamlit chat system
# -----------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    msg = user_input.strip()
    response = None

    # Small talk
    small = small_talk_response(msg)
    if small:
        response = small

    # Challenges
    if response is None and wants_challenge(msg):
        ch = random.choice(challenges)
        response = f"🧩 **Challenge - {ch['title']}**\n{ch['task']}\n💡 Hint: {ch['hint']}"
        st.session_state.last_challenge = ch

    # FAQ
    if response is None:
        faq_answer = find_faq_answer(msg)
        if faq_answer:
            response = faq_answer

    # Personality fallback
    if response is None:
        response = "Hmm… I’m not sure about that yet. Try asking about variables, lists, loops, or say 'challenge'."

    # Save messages
    st.session_state.history.append(("You", msg))
    st.session_state.history.append(("🤖 Agamemnon", response))

# Display chat history
for speaker, text in st.session_state.history:
    st.markdown(f"**{speaker}:** {text}")

# Optional: Interactive challenge submission
if st.session_state.last_challenge:
    st.write(f"Submit your code for: **{st.session_state.last_challenge['title']}**")
    user_code = st.text_area("Your Python code here:")
    if st.button("✅ Check Code"):
        checker_name = st.session_state.last_challenge.get("checker")
        if checker_name and checker_name in globals():
            result = globals()[checker_name](user_code)
            if result:
                st.success("Correct! 🎉")
            else:
                st.error("Hmm… not quite. Try again!")

# Clear chat
if st.button("🧹 Clear Chat"):
    st.session_state.history.clear()
    st.session_state.last_challenge = None
    st.session_state.last_topic = None
    st.experimental_rerun()
