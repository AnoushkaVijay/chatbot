import streamlit as st
from openai import OpenAI


OPENAI_CHAT_MODEL = "gpt-4o-mini"

if 'login' not in st.session_state:
    st.session_state.login = False

if 'user_id' not in st.session_state:
    st.session_state.user_id = False

    
if not st.session_state.login:
    st.error("Please LogIn using the Home page to use the ChatBot", icon = "🚨")
    st.stop()

# set openai key
client = OpenAI(api_key= st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = OPENAI_CHAT_MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})



