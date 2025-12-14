# backend/app_core.py  
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

# --- Define request model ---
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

# --- Initialize FastAPI ---
app = FastAPI(
    title="Customer Support Semantic Search API",
    description="Lightweight FastAPI + FAISS app for semantic search.",
    version="1.1",
)

# --- Lazy-loaded resources ---
model = None
index = None
answers = None

# --- Define paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_DIR = os.path.join(BASE_DIR, "embeddings")
answers_path = os.path.join(EMBEDDINGS_DIR, "answers.npy")
faiss_index_path = os.path.join(EMBEDDINGS_DIR, "faiss_index.index")

# --- Root endpoint ---
@app.get("/")
def read_root():
    return {"message": "Customer Support Semantic Search API is running."}


# --- Helper to load model and data on first request ---
def load_resources():
    global model, index, answers
    if model is None:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    if index is None:
        index = faiss.read_index(faiss_index_path)
    if answers is None:
        answers = np.load(answers_path, allow_pickle=True)


# --- Search endpoint ---
@app.post("/search")
def search(req: QueryRequest):
    # Ensure resources are loaded
    load_resources()

    # Encode query
    query_vector = model.encode([req.query], convert_to_numpy=True).astype("float32")

    # Search FAISS index
    distances, indices = index.search(query_vector, req.top_k)
    indices_list = indices[0].tolist()
    distances_list = distances[0].tolist()

    # Map indices to actual answer texts
    results = [answers[i] for i in indices_list]

    return {
        "query": req.query,
        "results": results,
        "distances": distances_list,
    }
