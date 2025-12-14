
NLP Customer Support Semantic Search (Retrieval-only question answering).

🔍 Overview:
An intelligent semantic search system for customer support, built with Sentence Transformers, FAISS, FastAPI, and Gradio, with the backend deployment on Render and frontend deployment on Hugging Face.  
Users can type natural-language questions and instantly receive the most relevant answers from historical support conversations.

🎯 Goal:
To demonstrate an end-to-end NLP pipeline — from data preprocessing and embedding generation to backend API deployment and interactive frontend — using real customer support data.

🗂️ Dataset
Source: Twitter Customer Support Dataset (Kaggle)
Processed into Q–A pairs of customer queries and support responses
Cleaned, vectorized, and indexed for semantic search


⚙️ Tech Stack:

| Component             | Tool                                       |
| --------------------- | ------------------------------------------ |
| **Language Model**    | `sentence-transformers (all-MiniLM-L6-v2)` |
| **Similarity Search** | `FAISS`                                    |
| **Backend API**       | `FastAPI` (deployed on Render)             |
| **Frontend UI**       | `Gradio` (deployed on Hugging Face Spaces) |
| **Data Source**       | Twitter → Q–A pairs from Kaggle dataset    |


🧩 Project Structure:

NLP_Customer_Support/
│
├── backend/          # FastAPI + FAISS backend (Render)
│   ├── app.py
│   ├── requirements.txt
│   └── data/, embeddings/
│
├── frontend/         # Gradio frontend (Hugging Face)
│   ├── ui.py
│   └── requirements.txt
│
└── NLP_customer_support.ipynb  # Data cleaning + embeddings


🚀 Deployment:

Backend: Render (FastAPI API endpoint)
Frontend: Hugging Face Spaces (Gradio app)
Integration: Frontend sends user queries to the backend /search endpoint via REST API

🧠 Key Features:

✅ Sentence embeddings via transformer models
✅ Semantic similarity search with FAISS
✅ Real-time Q–A matching
✅ Deployed, modular, and scalable architecture


🔗 Live Demo:

Frontend (Gradio): Hugging Face Space
Backend (FastAPI): Render App

References:

Sentence Transformers
FAISS
FastAPI
Gradio
Twitter Customer Support Dataset on Kaggle
