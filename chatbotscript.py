# python_faq_chatbot_v3.py
import streamlit as st
import random
import difflib

st.set_page_config(page_title="🐍 Agamemnon — Python Tutor & FAQ", page_icon="🤖", layout="centered")
st.title("🤖 Agamemnon — Python Tutor & FAQ")
st.write("Ask me about Python, request a challenge, or say something casual. (Try: 'Give me a challenge', 'What is a list?', 'Tell me something cool about Python')")

# -----------------------
# Helper data
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
    "what is if else": "`if/elif/else` lets your program choose actions based on conditions.",
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
    {"title": "Sum of Two Numbers", "task": "Ask the user for two numbers and print their sum.", "hint": "Use `input()` and convert to int: `int(input())`."},
    {"title": "Even or Odd", "task": "Read a number and print whether it's even or odd.", "hint": "Use `% 2` to check remainder."},
    {"title": "Reverse a String", "task": "Ask for a string and print it reversed.", "hint": "Use `s[::-1]` slicing."},
    {"title": "List Average", "task": "Given a list of numbers, compute their average.", "hint": "Use `sum(list) / len(list)`."},
    {"title": "Simple Counter Function", "task": "Write a function that counts how many times a specific item appears in a list.", "hint": "Loop through the list and increment a counter."},
]

casual_responses = {
    "casey": ["Ikaw na, Casey?"],
    "nino": ["Sig panghilabot dira dong"],
    "20th_century_girl": ["Best movie oat, 10/10 must watch."],
    "bai": ["Saman dong/dae"],
    "i miss her": ["Di na lage mo magbalik Corbin"],
    "unsa paman": ["Wa nako kaibaw dong."],
    "at sa bawat minuto": ["Ako'y di natuto"],
    "ipilit mang iba": ["Ako'y naghihintay sa'yo"],
    "10-fjk": ["THE GOATTT", "10-FJK>Others"],
    "izak": ["Ayaw ana Izak, bawal!"],
    "loberanis": ["Hi ms.! Ako imong 43rd student ms.", "Gimingaw kog f2f ms...."],
    "abadenas": ["Hi sir, pila akong grado sir? -Cabase"],
    "sir d": ["Hi sir plus points pls -Cabs"],
    "creator": ["ANG PINAKAGWAPO SA ROOM, SI KURT CABASE!!"],
    "greeting": ["Hey! What's up?", "Hello! How can I help you with Python today?", "Yo! Ready to code?"],
    "how_are_you": ["I'm a bot, but I'm running smoothly 😊", "All systems go! Ready to help."],
    "thanks": ["You're welcome!", "No problem — happy to help!", "Anytime!"],
    "cool_python": fun_facts,
}

# -----------------------
# Matching helpers
# -----------------------
def normalize(text: str) -> str:
    return text.lower().strip()

def find_faq_answer(message: str):
    msg = normalize(message)
    for key in faq:
        if key in msg:
            return faq[key]
    matches = difflib.get_close_matches(msg, list(faq.keys()), n=1, cutoff=0.6)
    if matches:
        return faq[matches[0]]
    for w in msg.split():
        close = difflib.get_close_matches(w, list(faq.keys()), n=1, cutoff=0.75)
        if close:
            return faq[close[0]]
    return None

def wants_challenge(message: str) -> bool:
    keywords = ["challenge", "task", "exercise", "problem", "give me a challenge", "practice"]
    msg = normalize(message)
    for k in keywords:
        if k in msg:
            return True
    for w in msg.split():
        if difflib.get_close_matches(w, keywords, n=1, cutoff=0.8):
            return True
    return False

def small_talk_response(message: str):
    msg = normalize(message)
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
# Streamlit chat system
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    msg = user_input.strip()
    response = None

    # 1) small talk
    small = small_talk_response(msg)
    if small:
        response = small

    # 2) challenge
    if response is None and wants_challenge(msg):
        ch = random.choice(challenges)
        response = f"🧩 **Challenge - {ch['title']}**\n\n{ch['task']}\n\n💡 Hint: {ch['hint']}"

    # 3) FAQ
    if response is None:
        faq_answer = find_faq_answer(msg)
        if faq_answer:
            response = faq_answer

    # 4) explicit creator ask
    if response is None and any(k in normalize(msg) for k in ["who made python", "who created python", "creator of python", "who created it"]):
        response = faq.get("who created python")

    # 5) casual_responses match
    if response is None:
        for key, value in casual_responses.items():
            if key.lower() in normalize(msg):
                response = random.choice(value)
                break

    # 6) personality / fallback
    if response is None:
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
        else:
            response = "Hmm… I’m not sure about that yet. Try asking about variables, lists, loops, or say 'challenge'."

    # Save messages
    st.session_state.history.append(("You", msg))
    st.session_state.history.append(("🤖 Agamemnon", response))

# Display chat history
for speaker, text in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {text}")
    else:
        st.markdown(f"**{speaker}:** {text}")

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.history.clear()
    st.experimental_rerun()
