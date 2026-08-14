"""
Lightweight RAG (Retrieval-Augmented Generation) Pipeline Boilerplate
Author: SpectraOne Solutions (https://spectraonesolutions.com/ai-automation)
Description: Production template demonstrating document chunking, semantic cosine similarity, and contextual augmentation.
"""

import numpy as np

# Sample Knowledge Base (Knowledge Chunks)
KNOWLEDGE_BASE = [
    {"id": 1, "text": "SpectraOne Solutions provides live, mentor-led bootcamps in AI Automation, QA, and Data Science."},
    {"id": 2, "text": "RAG architecture combines vector search with LLMs to provide factual, hallucinations-free answers."},
    {"id": 3, "text": "AI agents use the ReAct framework to reason, select tools, and execute workflows autonomously."},
    {"id": 4, "text": "Intelligent Document Processing extracts structured data from PDFs, invoices, and unstructured receipts."}
]

def mock_get_embedding(text: str) -> np.ndarray:
    """Simulates an embedding vector generation (e.g., text-embedding-3-small)."""
    np.random.seed(abs(hash(text)) % (2**32))
    vec = np.random.randn(128)
    return vec / np.linalg.norm(vec)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def retrieve_relevant_context(query: str, top_k: int = 2) -> list:
    query_vec = mock_get_embedding(query)
    scored_chunks = []
    
    for item in KNOWLEDGE_BASE:
        doc_vec = mock_get_embedding(item["text"])
        score = cosine_similarity(query_vec, doc_vec)
        scored_chunks.append((score, item["text"]))
        
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [chunk[1] for chunk in scored_chunks[:top_k]]

def generate_augmented_prompt(user_query: str) -> str:
    retrieved_docs = retrieve_relevant_context(user_query, top_k=2)
    context_str = "\n".join([f"- {doc}" for doc in retrieved_docs])
    
    prompt = f"""You are an enterprise AI assistant. Answer the user query strictly based on the provided context.

### CONTEXT:
{context_str}

### USER QUERY:
{user_query}

### ANSWER:"""
    return prompt

if __name__ == "__main__":
    query = "How do AI agents automate workflows?"
    final_prompt = generate_augmented_prompt(query)
    print("=" * 65)
    print("🤖 GENERATED RAG PROMPT READY FOR LLM EXECUTION:")
    print("=" * 65)
    print(final_prompt)
