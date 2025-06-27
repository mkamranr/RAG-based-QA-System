from app.vector_store import load_vector_store
from app.config import OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY

def query_rag(question: str, k: int = 4) -> str:
    vector_store = load_vector_store()
    docs = vector_store.similarity_search(question, k=k)

    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""Answer the following question using the context below:
    
Context:
{context}

Question: {question}
Answer:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response["choices"][0]["message"]["content"]
