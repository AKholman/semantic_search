# app.py (Frontend)

import gradio as gr
import requests
import time

# -----------------------------
# Backend URL (UPDATED FOR NEW SPACE SUBDOMAIN)
# -----------------------------
BACKEND_URL = "https://Alex-Khol-semantic-search-customer-support-backend.hf.space/search"

# -----------------------------
# Function to call backend API
# -----------------------------
def semantic_search(query, top_k):
    """
    Sends the query to the FastAPI backend and returns top text answers.
    """
    payload = {"query": query, "top_k": top_k}
    try:
        # Increase timeout to handle slower responses
        # NOTE: Using a shorter timeout for general API responsiveness
        response = requests.post(BACKEND_URL, json=payload, timeout=60) 
        
        if response.status_code == 200:
            data = response.json()
            return "\n\n".join(data["results"])
        else:
            # Display detailed error if the request succeeds but the status code is not 200
            return f"Error {response.status_code}: {response.text}"
        
    except requests.exceptions.RequestException as e:
        # Handle connection errors (timeout, DNS failure, etc.)
        return f"Connection error: Failed to reach backend API. Details: {e}"

# -----------------------------
# Gradio Interface (The corrected, complete code block)
# -----------------------------
iface = gr.Interface(
    # 1. The function to call when the user submits
    fn=semantic_search,
    
    # 2. The input components (must match the function arguments: query, top_k)
    inputs=[
        gr.Textbox(
            label="Enter your customer question",
            placeholder="E.g., How do I reset my password?",
            lines=3  # Allow for a multi-line query
        ),
        gr.Slider(
            minimum=1, 
            maximum=10, 
            value=3, 
            step=1, 
            label="Top K Results (Number of answers to retrieve)"
        )
    ],
    
    # 3. The output component (must match the function return: a single string)
    outputs=gr.Textbox(
        label="Top Relevant Answers",
        lines=10,
        show_copy_button=True
    ),
    
    # Optional arguments for UI styling
    title="Customer Support Semantic Search Assistant",
    description="Ask a question to retrieve the most relevant answers from the backend knowledge base via a FastAPI API call."
)

# -----------------------------
# Launch the Gradio app
# -----------------------------
if __name__ == "__main__":
    # Launch on the default port 7860
    # In Hugging Face Spaces, it will automatically launch correctly without share=True
    iface.launch()