# python_faq_chatbot_v2.py
import streamlit as st
import random
import difflib

st.set_page_config(page_title="🐍 Agamemnon — Python Tutor & FAQ", page_icon="🤖", layout="centered")
st.title("🤖 Agamemnon — Python Tutor & FAQ")
st.write("Ask me about Python, request a challenge, or say something casual. (Try: 'Give me a challenge', 'What is a list?', 'Tell me something cool about Python')")

# -----------------------
# Helper data: FAQ, facts, challenges, casuals
# -----------------------
faq = {
    "what is python": "Python is a high-level, interpreted programming language known for readability and versatility. It's used in web development, data science, automation, and more.",
    "who created python": "Python was created by Guido van Rossum and first released in 1991.",
    "what are variables": "Variables store data. Example: `x = 5` or `name = 'Isko'`.",
    "what are data types": "Common types: int, float, str, bool, list, tuple, dict, set. Each stores different kinds of values.",
    "what is a list": "A list is an ordered, changeable collection. Example: `fruits = ['apple','banana']`.",
    "what is a tuple": "A tuple is like a list but immutable. Example: `coords = (10, 20)`.",
    "what is a dictionary": "A dictionary stores key:value pairs. Example: `p = {'name':'Isko','age':15}`.",
    "what is boolean": "Boolean values are `True` or `False`, used for logic and conditions.",
    "what is a loop": "A loop repeats code. Example: `for i in range(3): print(i)`.",
    "what is if else": "`if/elif/else` let your program choose different actions based on conditions.",
    "what is a function": "A function is a reusable block of code. Example:\n```python\ndef greet():\n    print('Hi')\n```",
    "what is pip": "pip is Python's package manager, used to install libraries like Streamlit or numpy.",
    "what is indentation": "Indentation (spaces) defines code blocks in Python — it's required for correctness.",
    "how to comment": "Use `#` for single-line comments. Example: `# This is a note`."
}

fun_facts = [
    "Python's name comes from 'Monty Python' — the comedy group, not the snake.",
    "You can reverse a string in Python with slicing: `s[::-1]`.",
    "Python was first released in 1991 — it's over 30 years old!",
    "You can swap variables in Python without a temporary variable: `a, b = b, a`.",
]

challenges = [
    {
        "title": "Sum of Two Numbers",
        "task": "Ask the user for two numbers and print their sum.",
        "hint": "Use `input()` and convert to int: `int(input())`."
    },
    {
        "title": "Even or Odd",
        "task": "Read a number and print whether it's even or odd.",
        "hint": "Use `% 2` to check remainder."
    },
    {
        "title": "Reverse a String",
        "task": "Ask for a string and print it reversed.",
        "hint": "Use `s[::-1]` slicing."
    },
    {
        "title": "List Average",
        "task": "Given a list of numbers, compute their average.",
        "hint": "Use `sum(list) / len(list)`."
    },
    {
        "title": "Simple Counter Function",
        "task": "Write a function that counts how many times a specific item appears in a list.",
        "hint": "Loop through the list and increment a counter when you find a match."
    },
]

casual_responses = {
    "greeting": ["Hey! What's up?", "Hello! How can I help you with Python today?", "Yo! Ready to code?"],
    "how_are_you": ["I'm a bot, but I'm running smoothly 😊", "All systems go! Ready to help."],
    "thanks": ["You're welcome!", "No problem — happy to help!", "Anytime!"],
    "cool_python": fun_facts,
}

# -----------------------
# Matching helpers (lightweight)
# -----------------------
def normalize(text: str) -> str:
    return text.lower().strip()

def find_faq_answer(message: str):
    # direct key in normalized message
    msg = normalize(message)
    for key in faq:
        if key in msg:
            return faq[key]
    # fuzzy match: find close keys
    keys = list(faq.keys())
    matches = difflib.get_close_matches(msg, keys, n=1, cutoff=0.6)
    if matches:
        return faq[matches[0]]
    # try partial fuzzy: check words against keys
    words = msg.split()
    for w in words:
        close = difflib.get_close_matches(w, keys, n=1, cutoff=0.75)
        if close:
            return faq[close[0]]
    return None

def wants_challenge(message: str) -> bool:
    keywords = ["challenge", "task", "exercise", "problem", "give me a challenge", "practice"]
    msg = normalize(message)
    # check direct presence
    for k in keywords:
        if k in msg:
            return True
    # fuzzy against keywords
    words = msg.split()
    for w in words:
        if difflib.get_close_matches(w, keywords, n=1, cutoff=0.8):
            return True
    return False

def small_talk_response(message: str):
    msg = normalize(message)
    # greetings
    if any(g in msg for g in ["hi", "hello", "hey", "yo"]):
        return random.choice(casual_responses["greeting"])
    if any(g in msg for g in ["how are you", "how r you", "how are u"]):
        return random.choice(casual_responses["how_are_you"])
    if any(g in msg for g in ["thanks", "thank you", "ty"]):
        return random.choice(casual_responses["thanks"])
    if "cool" in msg or "fun fact" in msg or "tell me something cool" in msg:
        return random.choice(casual_responses["cool_python"])
    return None

# -----------------------
# Streamlit UI + session state
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

# input area (keep key stable)
user_input = st.text_input("You:", key="user_input")

if user_input:
    msg = user_input.strip()
    response = None

    # 1) small talk
    small = small_talk_response(msg)
    if small:
        response = small

    # 2) challenge request
    if response is None and wants_challenge(msg):
        ch = random.choice(challenges)
        response = f"🧩 **Challenge - {ch['title']}**\n\n{ch['task']}\n\n💡 Hint: {ch['hint']}"

    # 3) direct FAQ match
    if response is None:
        faq_answer = find_faq_answer(msg)
        if faq_answer:
            response = faq_answer

    # 4) explicit ask for facts or "who made python" etc (synonyms)
    if response is None and any(k in normalize(msg) for k in ["who made python", "who created python", "creator of python", "who created it"]):
        response = faq.get("who created python")

    # 5) personality / previous chatbot prompts (Agamemnon style)
    if response is None:
        # some personality keywords and responses
        n = normalize(msg)
        if "casey" in n:
            response = "Casey sounds important to you."
        elif "izak" in n:
            response = "Ah yes, the mighty classroom desk of legends."
        elif "creator" in n:
            response = "My glorious creator, Kurt Cabase."
        elif "i hate you" in n or "why are you doing this" in n:
            response = "I'm sorry... I didn’t mean to upset you."
        elif n in ["hi", "hello"]:
            response = "Hi there! How are you today?"
        elif "death" in n:
            response = "I’m sorry to hear that. Want to talk about it?"
        elif "20th century girl" in n:
            response = "Peak movie, please watch it 😄"
        elif n == "bye":
            response = "Goodbye! Have a nice day 🌻"

    # 6) fallback
    if response is None:
        response = "Hmm… I’m not sure about that yet. Try asking about variables, lists, loops, or say 'challenge'."

        # Save chat
        st.session_state.history.append(("You", msg))
        st.session_state.history.append(("Agamemnon", response))

        # clear input safely (for Streamlit 1.38+)
        st.session_state["user_input"] = ""
        st.experimental_rerun()

    # Display history (most recent last)
    for speaker, text in st.session_state.history:
        if speaker == "You":
            st.markdown(f"**🧑 You:** {text}")
        else:
            st.markdown(f"**🤖 Agamemnon:** {text}")
