from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

def create_vector_store(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs_splits = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs_splits, embeddings)
    
    return db
