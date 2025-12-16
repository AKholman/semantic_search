# backend/app_core.py  app core 

from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path
from contextlib import asynccontextmanager
import os

# -----------------------------
# Lazy-loaded globals (Model, Index, and Answers)
# We will use the app.state object to share them, but globals are needed for
# the lifespan function scope
model_instance = None
faiss_index_instance = None
answers_array_instance = None

# -----------------------------
# Paths (HF Spaces persistent storage)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
EMBEDDINGS_DIR = BASE_DIR / "embeddings"
ANSWERS_PATH = EMBEDDINGS_DIR / "answers.npy"
FAISS_INDEX_PATH = EMBEDDINGS_DIR / "faiss_index.index"

# Ensure directory exists (This should run at module load)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Example seed data (MUST BE DEFINED HERE)
# -----------------------------
def load_seed_data():
    """
    Replace this with your final data source.
    """
    return [
        "You can reset your password from the settings page.",
        "Our support team is available 24/7 via email.",
        "Refunds are processed within 5–7 business days.",
        "You can update your billing information in your account dashboard.",
        "Please contact support if you encounter login issues."
    ]

# -----------------------------
# Build embeddings (RUNS ONLY IF FILES ARE MISSING - NOW DISABLED)
# -----------------------------
def build_embeddings():
    print("🔧 Building embeddings from scratch...")

    # Load model only for building
    local_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    texts = load_seed_data()
    local_answers = np.array(texts)

    embeddings = local_model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    ).astype("float32")

    dim = embeddings.shape[1]
    local_index = faiss.IndexFlatL2(dim)
    local_index.add(embeddings)

    # Persist to disk
    np.save(ANSWERS_PATH, local_answers)
    faiss.write_index(local_index, str(FAISS_INDEX_PATH))

    print("✅ Embeddings built and saved to disk")


# -----------------------------
# Application Lifespan (The critical fix!)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs BEFORE the application starts accepting requests (STARTUP)
    global model_instance, faiss_index_instance, answers_array_instance
    
    # 1. Load the sentence transformer model (heavy)
    print("⏳ Loading Sentence Transformer Model...")
    model_instance = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    # 2. Check for embeddings and build if necessary (heavy) - COMMENTED OUT
    # This logic is DISABLED because the files must be manually uploaded to avoid startup timeouts.
    """
    if not FAISS_INDEX_PATH.exists() or not ANSWERS_PATH.exists():
        build_embeddings()
    """

    # 3. Load the FAISS index and Answers (heavy)
    print("⏳ Loading FAISS Index and Answers...")
    
    # This will now fail fast if the manual upload hasn't been completed.
    try:
        faiss_index_instance = faiss.read_index(str(FAISS_INDEX_PATH))
        answers_array_instance = np.load(ANSWERS_PATH, allow_pickle=True)
    except Exception as e:
        print(f"FATAL ERROR: Could not load embeddings. Ensure files are manually uploaded. Error: {e}")
        # Re-raise the exception to force the container to fail the startup health check
        raise RuntimeError("Missing pre-generated embedding files.") from e


    print("🎉 All heavy resources loaded. App is ready.")

    # Store resources in app.state for access in endpoints
    app.state.model = model_instance
    app.state.index = faiss_index_instance
    app.state.answers = answers_array_instance
    
    yield # Application starts receiving requests after this line

    # This runs when the application is shutting down (SHUTDOWN)
    print("👋 Shutting down application...")


# -----------------------------
# FastAPI app initialization
# -----------------------------
app = FastAPI(
    title="Customer Support Semantic Search API",
    description="FastAPI + FAISS semantic search (HF Spaces friendly)",
    version="1.3",
    lifespan=lifespan # Attach the lifespan context manager
)

# -----------------------------
# Request model
# -----------------------------
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

# -----------------------------
# Health check (will now wait for lifespan to complete)
# -----------------------------
@app.get("/")
def root():
    # The health check can now be guaranteed to run after model is loaded
    return {"status": "Customer Support Semantic Search API is running"}

# -----------------------------
# Search endpoint (Simplified: Resources are guaranteed to be loaded)
# -----------------------------
@app.post("/search")
def search(req: QueryRequest):
    # Retrieve resources from app.state (guaranteed to be loaded)
    model = app.state.model
    index = app.state.index
    answers = app.state.answers

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