from fastapi import FastAPI
from qa import ask

app = FastAPI(title="Enterprise RAG Demo")

@app.get("/ask")
def ask_question(q: str):
    result = ask(q)
    return {
        "question": q,
        "answer": result["result"],
        "sources": [
            doc.metadata.get("source", "")
            for doc in result["source_documents"]
        ]
    }