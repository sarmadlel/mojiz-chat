from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
import os
import pinecone 
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st
from dotenv import load_dotenv




load_dotenv()


PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENVIRONMENT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

directory = 'data'

def doc_preprocessing(directory):
    loader = DirectoryLoader(directory)
    docs = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=0
    )
    docs_split = text_splitter.split_documents(docs)
    return docs_split


@st.cache_resource
def embedding_db():
    # we use the openAI embedding model
    embeddings = OpenAIEmbeddings()
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV
    )
    docs_split = doc_preprocessing(directory)
    doc_db = Pinecone.from_documents(
        docs_split, 
        embeddings, 
        index_name='mojiz-book'
    )
    return doc_db

""" from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
import os
import pinecone 
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st
from dotenv import load_dotenv
import time  # Import the time module

load_dotenv()

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENVIRONMENT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

def doc_preprocessing():
    loader = DirectoryLoader(
        'C:/Users/HF/Documents/Data Pilot/New Project/book1',
        glob='**/*.pdf',     # only the PDFs
        show_progress=True
    )
    docs = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=3000, 
        chunk_overlap=200
    )
    docs_split = text_splitter.split_documents(docs)
    return docs_split

@st.cache_resource
def embedding_db():
    # We use the openAI embedding model
    embeddings = OpenAIEmbeddings()
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENV
    )
    docs_split = doc_preprocessing()
    doc_db = Pinecone.from_documents(
        docs_split[0:1],  # Add only the first chunk
        embeddings, 
        index_name='mojiz-book'
    )

    # Wait for 70 seconds before adding the next chunk
    time.sleep(1)

    # Add the next chunk
    doc_db.add_documents(docs_split[1:])

    return doc_db """
