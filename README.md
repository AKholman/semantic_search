
NLP Customer Support Semantic Search (Retrieval-only question answering).

📌 Overview

This project implements a production-oriented semantic search system for customer support, enabling users to retrieve the most relevant historical support responses using natural language queries.

The system is built using Sentence Transformers for semantic embeddings and FAISS for high-performance vector similarity search, exposed via a FastAPI backend and accessed through an interactive Gradio frontend.

The architecture follows a clean separation of concerns, with the backend and frontend deployed as independent Hugging Face Spaces, communicating via REST APIs.


🎯 Objective

To demonstrate an end-to-end NLP retrieval pipeline, covering:

Data preprocessing and question–answer pair extraction
Semantic embedding generation
Vector indexing and similarity search
Robust backend API deployment
Interactive frontend integration
The project emphasizes real-world ML system design practices, including reproducibility, environment isolation, and deployment safety.


🗂️ Dataset

Source: Twitter Customer Support Dataset (Kaggle);  
Content: Historical customer queries and corresponding support responses;   
Processing:  
    Cleaned and normalized text;   
    Converted into question–answer pairs;  
    Embedded using transformer-based sentence encoders;   
    Indexed using FAISS for efficient semantic retrieval;


⚙️ Tech Stack:

| Component             | Tool                                         |
| --------------------- | -------------------------------------------- |
| **Language Model**    | `sentence-transformers (all-MiniLM-L6-v2)`   |
| **Similarity Search** | `FAISS` (CPU)                                |
| **Backend API**       | `FastAPI` on Docker-based HF  spaces         |
| **Frontend UI**       | `Gradio` on HF Spaces                        |
| **Data Source**       | Twitter → Q–A pairs from Kaggle dataset      |

Loading / rebuilding embeddings;  
FAISS similarity search;  
Serving search results via REST endpoints;  


🧩 Project Structure:

NLP_Customer_Support Semantic Search/
│
├── backend/                     # FastAPI + FAISS backend (HF Space - Docker)
│   ├── app_core.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── embeddings/              # Runtime-generated (not tracked in Git)
│
├── frontend/                    # Gradio UI (HF Space)
│   ├── app.py
│   └── requirements.txt
│
└── NLP_customer_support.ipynb   # Data preprocessing + embedding pipeline

Note:
FAISS index files and NumPy embeddings are not committed to Git.
They are either generated at runtime or manually transferred to the backend Space to ensure compatibility with the execution environment.



🚀 Deployment Strategy:   
   
Backend:    
    Deployed as a Docker-based Hugging Face Space;   
    Loads or rebuilds FAISS indexes safely during startup;   
    Exposes a /search REST endpoint;   
     
Frontend:   
    Deployed as a Gradio Hugging Face Space;   
    Sends user queries to the backend via HTTP requests;    
    Displays top-K semantically similar responses;    
   
Integration:   
    Stateless REST communication;   
    Frontend and backend can be scaled or updated independently;   


🧠 Key Features

✅ Transformer-based sentence embeddings;  
✅ Fast semantic similarity search using FAISS;   
✅ Retrieval-only question answering (no generative hallucinations);  
✅ Clean separation of frontend and backend services;   
✅ Deployment-safe handling of ML artifacts;    
✅ Production-aware ML system design;    


🔗 Live Demo:   
Frontend (Gradio UI): Hugging Face Space;   
Backend (FastAPI API): Hugging Face Docker Space;   


📚 References:   
Sentence Transformers;   
FAISS;     
FastAPI;   
Gradio;     
Twitter Customer Support Dataset (Kaggle).


💡 Final Note:

This project intentionally avoids committing binary ML artifacts to version control and instead rebuilds or loads them at runtime, reflecting best practices in production machine learning systems and cloud-native deployment environments.