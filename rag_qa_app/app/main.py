from fastapi import FastAPI, UploadFile, File, Form
from app.document_loader import load_and_split_document
from app.vector_store import create_vector_store
from app.rag import query_rag
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    chunks = load_and_split_document(file_path)
    create_vector_store(chunks)
    return {"message": "Document uploaded and indexed successfully."}

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    try:
        answer = query_rag(question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
