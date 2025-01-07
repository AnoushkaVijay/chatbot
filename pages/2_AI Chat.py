import streamlit as st
from openai import OpenAI
from RAG import get_similar_context, streaming_question_answering


OPENAI_CHAT_MODEL = "gpt-4o-mini"

if 'login' not in st.session_state:
    st.session_state.login = False

if 'user_id' not in st.session_state:
    st.session_state.user_id = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.login:
    st.error("Please LogIn using the Home page to use the ChatBot", icon = "🚨")
    st.stop()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        query_meta = {"user_id": st.session_state.user_id}
        pinecone_context = get_similar_context(prompt, query_meta)
        print(pinecone_context)
        response = st.write_stream(streaming_question_answering(prompt, pinecone_context))
    st.session_state.messages.append({"role": "assistant", "content": response})
