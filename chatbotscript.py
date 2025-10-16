import streamlit as st

st.title("🤖 Agamemnon – Your Friendly Chatbot")

# A text input box for the user
user_input = st.text_input("You:", "")

# When the user types something
if user_input:
    user = user_input.lower()

    if user in ["hi", "hello"]:
        response = "Hi there! How are you today?"
    elif "death" in user:
        response = "I’m sorry to hear that. Want to talk about it?"
    elif "20th century girl" in user:
        response = "Peak movie, please watch it 😄"
    elif user == "bye":
        response = "Goodbye! Have a nice day 🌻"
    elif "creator" in user:
        response = "My glorious king, Kurt Cabase."
    elif "i hate you" in user or "why are you doing this" in user:
        response = "I'm sorry..."
    elif "casey" in user:
        response = "I hate Casey so much."
    elif "izak" in user:
        response = "Why is he so black?"  # You might want to remove or rephrase this for class use.
    elif "ikr" in user:
        response = "Yas gurlll"
    else:
        response = "Hmm… I’m not sure how to respond to that."

    st.markdown(f"**Agamemnon:** {response}")
