import os
from langchain_groq import ChatGroq

# Verify Groq API authentication presence
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("CRITICAL: GROQ_API_KEY environment variable is not configured.")

# Switch to the stable production Llama 3.3 70B model identifier
llm = ChatGroq(
    temperature=0.2,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=GROQ_API_KEY
)