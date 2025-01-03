import streamlit as st
from openai import OpenAI

if 'login' not in st.session_state:
    st.session_state.login = False

if 'user_id' not in st.session_state:
    st.session_state.user_id = False

    
if not st.session_state.login:
    st.error("Please LogIn using the Home page to upload the diary entries", icon = "🚨")
    st.stop()

# Show title and description.
st.title("🧠 MemoryLane")



#Diary uploading as a txt or pdf file
#multiple files allowed
uploaded_files = st.file_uploader(
    "Choose a txt or pdf file(s)", type = ['pdf', 'txt'], accept_multiple_files=True
)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)

