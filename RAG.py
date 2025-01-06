import PyPDF2
import os
import streamlit as st
from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from pinecone import Pinecone
import uuid


NAMESPACE_KEY = "MemoryLane"
TEXT_MODEL = "text-embedding-ada-002"
QA_MODEL = "gpt-4o-mini"

# '''
# COMMON_TEMPLATE = """
# "Use the following pieces of context to answer the question at the end with human readable answer."
# "Please do not use data outside the context to answer any questions."
# "If the answer is not in the given context, just say that you don't have enough context."
# "don't try to make up an answer. "
# "\n\n"
# {context}
# "\n\n"
# Question: {question}
# "n"
# "Helpful answer:   "
# """
# '''

COMMON_TEMPLATE = """

You are an expert being answered based on given context.

You goal is to answer a question posed by the user or explain what is posed by the user.

Here is the user posted query.

{question}

Use the folowing guidenlines to answer user questions.

1. First check whether user is asking a question or greeting, or an explanation.

2. If it is a greeting, please greet appropriately.

3. If it is an explanation, use your knowledge to answer the question without the context.

4. If it is a question, use the given context to answer.

To answer question, use this context:

{context}

When answering questions, follow these guidelines:

1. Use only the information provided in the context.

2. Do not introduce external information or make assumptions beyond what is explicitly stated in the context.
"""

# keys
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
os.environ["INDEX_HOST"] = st.secrets["INDEX_HOST"]

# pinecone setup
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(host=os.environ["INDEX_HOST"])
# create client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

#store embeddings in pinecone
def get_openai_embeddings(text: str) -> list[float]:
    response = client.embeddings.create(input=f"{text}", model=TEXT_MODEL)

    return response.data[0].embedding


# function query similar chunks
def query_response(query_embedding, meta_query, k = 2, namespace_ = NAMESPACE_KEY):
    query_response_ = index.query(
        namespace=namespace_,
        vector=query_embedding,
        top_k=k,
        include_values=False,
        include_metadata=True,
        metadata = meta_query
    )

    return query_response_


def extract_text_from_pdf(pdf_path):
    pdf_text = ""
    # read the pdf
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # extract the text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()

    final_text = pdf_text.replace("\n", " ")
    
    return final_text


# function to store embeddings
def upsert_embeddings(embeddings, meta_data, namespace_ = NAMESPACE_KEY):
    vector_id = str(uuid.uuid4())
    upsert_response = index.upsert(
    vectors=[
        (vector_id, embeddings, meta_data),
    ],
    namespace=namespace_
    )

    return upsert_response


def content_extractor(similar_data):
    top_values = similar_data["matches"]
    # get the text out
    text_content = [sub_content["metadata"]["text"] for sub_content in top_values]
    return " ".join(text_content)


def get_model():
    model = ChatOpenAI(model=QA_MODEL, api_key=os.environ["OPENAI_API_KEY"])
    return model


def get_similar_context(question: str, meta_dict: dict):
    # get the query embeddings
    quer_embed_data = get_openai_embeddings(question)

    # query the similar chunks
    similar_chunks = query_response(quer_embed_data, meta_dict)

    # extract the similar text data
    similar_content = content_extractor(similar_chunks)

    return similar_content


def streaming_question_answering(query_question: str, context_text: str,  template: str = COMMON_TEMPLATE):
    prompt = ChatPromptTemplate.from_template(template)
    model = get_model()
    output_parser = StrOutputParser()

    # create the chain
    chain = prompt | model | output_parser

    # get the answer
    return chain.stream({"context": context_text, "question": query_question})