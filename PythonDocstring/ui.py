import streamlit as st
from main import genai_engine, write_conversation_to_file

st.title("AI-Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

conversation = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.text_input("What is up?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    conversation.append(("user", prompt))
    response = genai_engine(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    conversation.append(("assistant", response))

filename = "C:/Users/S561633/Documents/PythonDocstring/test.txt"
if st.button("Save Conversation to File"):
    if write_conversation_to_file(conversation, filename):
        st.success(f"Conversation saved to {filename}")
    else:
        st.error("Failed to save conversation to file")
