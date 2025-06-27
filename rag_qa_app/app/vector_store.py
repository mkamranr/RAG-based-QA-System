import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from app.config import EMBEDDING_MODEL_NAME, VECTOR_STORE_DIR

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

def create_vector_store(chunks):
    db = FAISS.from_documents(chunks, embedding=embeddings)
    db.save_local(VECTOR_STORE_DIR)

def load_vector_store():
    if not os.path.exists(VECTOR_STORE_DIR):
        raise Exception("Vector DB not found. Upload document first.")
    return FAISS.load_local(VECTOR_STORE_DIR, embeddings)
