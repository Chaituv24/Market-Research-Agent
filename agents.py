import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from config import llm
from state import ResearchState
from langchain_core.messages import HumanMessage
from vector_storage import query_vector_dataset, save_to_vector_dataset

def scraper_node(state: ResearchState) -> Dict[str, Any]:
    """Agent 1: Evaluates Vector Database before running a web-scraping task."""
    topic = state["topic"]
    
    # Check vector dataset first
    existing_data = query_vector_dataset(topic)
    if existing_data:
        return {"raw_data": "CACHE_HIT", "filtered_data": existing_data}
        
    print(f"[Scraper Agent] Gathering fresh web data for: {topic}")
    search_url = f"https://html.duckduckgo.com/html/?q={topic}+competitor+pricing"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        snippets = [link.text.strip() for link in soup.find_all('a', class_='result__snippet')][:5]
        raw_text = "\n\n".join(snippets)
    except Exception as e:
        raw_text = f"Error during live scraping extraction: {str(e)}"
        
    return {"raw_data": raw_text}


def filter_node(state: ResearchState) -> Dict[str, Any]:
    """Agent 2: Extracts competitor insights or short-circuits on a Vector DB hit."""
    if state.get("raw_data") == "CACHE_HIT":
        print("[Filter Agent] Vector dataset hit! Skipping LLM data-cleaning step.")
        return {"filtered_data": state["filtered_data"]}
        
    print("[Filter Agent] Extracting competitive insights from fresh raw text...")
    prompt = f"""
    You are an expert Data Analyst Agent. Analyze the following web search snippets regarding '{state['topic']}'.
    Extract key features, competitor names, pricing structures, and core market patterns. Clean out fluff.
    
    Raw Data:
    {state['raw_data']}
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    filtered_output = response.content
    
    # Save to Vector DB dataset for future execution speed-ups
    save_to_vector_dataset(state["topic"], filtered_output)
    
    return {"filtered_data": filtered_output}


def formatter_node(state: ResearchState) -> Dict[str, Any]:
    """Agent 3: Transforms filtered structured notes into polished markdown output."""
    print("[Formatter Agent] Generating formal executive market report...")
    prompt = f"""
    You are a Senior Market Research Executive. Take the filtered market insights provided below and compile them into a comprehensive, professional, markdown-formatted Market Research Report for: '{state['topic']}'.
    
    Filtered Insights:
    {state['filtered_data']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_report": response.content}