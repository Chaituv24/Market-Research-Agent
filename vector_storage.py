import os
import chromadb
from chromadb.utils import embedding_functions

# Set up local directory storage path for the persistent dataset
DB_PATH = os.path.join(os.path.dirname(__file__), "market_research_db")
chroma_client = chromadb.PersistentClient(path=DB_PATH)

# Use default lightweight embedding function
embedding_func = embedding_functions.DefaultEmbeddingFunction()

# Access or initialize our structural collection
collection = chroma_client.get_or_create_collection(
    name="competitor_insights",
    embedding_function=embedding_func
)

def query_vector_dataset(topic: str) -> str:
    """Queries Vector DB to see if relevant historical records exist."""
    print(f"[Vector DB] Checking historical dataset for: '{topic}'")
    
    results = collection.query(
        query_texts=[topic],
        n_results=1,
        include=["documents", "distances"]
    )
    
    if results and results['documents'] and results['documents'][0]:
        distance = results['distances'][0][0]
        # Low distance metric (< 0.4) indicates high semantic match accuracy
        if distance < 0.4:
            print("[Vector DB] Relevant historical data found! Bypassing live processing pipeline.")
            return results['documents'][0][0]
            
    print("[Vector DB] No relevant historical data found. Initiating live retrieval.")
    return ""

def save_to_vector_dataset(topic: str, filtered_data: str):
    """Saves high-quality processed insights into the persistent dataset."""
    document_id = f"id_{topic.replace(' ', '_').lower()}"
    collection.add(
        documents=[filtered_data],
        metadatas=[{"topic": topic}],
        ids=[document_id]
    )
    print(f"[Vector DB] Successfully saved filtered dataset entry for '{topic}'.")