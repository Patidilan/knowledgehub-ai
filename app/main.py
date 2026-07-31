from fastapi import FastAPI

app = FastAPI(
    title="KnowledgeHub AI",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "Welcome to KnowledgeHub AI 🚀"
    }