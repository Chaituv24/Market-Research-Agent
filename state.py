from typing import TypedDict

class ResearchState(TypedDict):
    topic: str            # Core user input string
    raw_data: str         # Populated by Scraper Node (or set to "CACHE_HIT")
    filtered_data: str    # Populated by Filter Node (or pulled directly from Vector DB)
    final_report: str     # Populated by Formatter Node