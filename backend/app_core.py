# backend/app_core.py

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path
import os

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(
    title="Customer Support Semantic Search API",
    description="FastAPI + FAISS semantic search (HF Spaces friendly)",
    version="1.2",
)

# -----------------------------
# Request model
# -----------------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

# -----------------------------
# Paths (HF Spaces persistent storage)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
EMBEDDINGS_DIR = BASE_DIR / "embeddings"
ANSWERS_PATH = EMBEDDINGS_DIR / "answers.npy"
FAISS_INDEX_PATH = EMBEDDINGS_DIR / "faiss_index.index"

# Ensure directory exists
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Lazy-loaded globals
# -----------------------------
model = None
index = None
answers = None

# -----------------------------
# Example seed data (replace later)
# -----------------------------
def load_seed_data():
    """
    Replace this with:
    - Wikidata
    - FAQ CSV
    - Database
    - JSON knowledge base
    """
    return [
        "You can reset your password from the settings page.",
        "Our support team is available 24/7 via email.",
        "Refunds are processed within 5–7 business days.",
        "You can update your billing information in your account dashboard.",
        "Please contact support if you encounter login issues."
    ]

# -----------------------------
# Build embeddings (RUNS ONCE)
# -----------------------------
def build_embeddings():
    global model, index, answers

    print("🔧 Building embeddings from scratch...")

    if model is None:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    texts = load_seed_data()
    answers = np.array(texts)

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    ).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Persist to disk (HF Spaces allows this)
    np.save(ANSWERS_PATH, answers)
    faiss.write_index(index, str(FAISS_INDEX_PATH))

    print("✅ Embeddings built and saved")

# -----------------------------
# Load or build resources
# -----------------------------
def load_resources():
    global model, index, answers

    if model is None:
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    if not FAISS_INDEX_PATH.exists() or not ANSWERS_PATH.exists():
        build_embeddings()
    else:
        if index is None:
            index = faiss.read_index(str(FAISS_INDEX_PATH))
        if answers is None:
            answers = np.load(ANSWERS_PATH, allow_pickle=True)

# -----------------------------
# Health check
# -----------------------------
@app.get("/")
def root():
    return {"status": "Customer Support Semantic Search API is running"}

# -----------------------------
# Search endpoint
# -----------------------------
@app.post("/search")
def search(req: QueryRequest):
    load_resources()

    query_vector = model.encode(
        [req.query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(query_vector, req.top_k)

    results = [answers[i] for i in indices[0]]

    return {
        "query": req.query,
        "results": results,
        "distances": distances[0].tolist(),
    }
