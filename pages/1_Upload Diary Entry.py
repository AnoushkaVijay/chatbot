import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

from RAG import extract_text_from_pdf, get_openai_embeddings, upsert_embeddings


FILE_NAME = "uploaded_file.pdf"


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
    "Choose a pdf file", type = ['pdf']
)

if uploaded_files:
    with open(FILE_NAME, "wb") as pdf_file:
        pdf_file.write(uploaded_files.getbuffer())

    #read the pdf data
    pdf_text = extract_text_from_pdf(FILE_NAME)
    st.write(pdf_text)


    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=400,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )

    # chunk the texts
    chunk_texts = text_splitter.create_documents([pdf_text])

    with st.spinner("Saving the information..."):
        for chunk_document in chunk_texts:
            chunk_text_data = chunk_document.page_content
            # get embeddings
            embeddings = get_openai_embeddings(chunk_text_data)
            # create metadata
            meta_creator = {"text": chunk_text_data, "user_id": st.session_state.user_id}
            # store embeddings
            emb_response = upsert_embeddings(embeddings, meta_creator)

    st.toast("Data saved to the memory")

