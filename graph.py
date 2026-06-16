from langgraph.graph import StateGraph, END
from state import ResearchState
from agents import scraper_node, filter_node, formatter_node

# Create state graph blueprint schema
workflow = StateGraph(ResearchState)

# Append node logical modules
workflow.add_node("scraper", scraper_node)
workflow.add_node("filter", filter_node)
workflow.add_node("formatter", formatter_node)

# Map edge paths (Scraper -> Filter -> Formatter -> End)
workflow.set_entry_point("scraper")
workflow.add_edge("scraper", "filter")
workflow.add_edge("filter", "formatter")
workflow.add_edge("formatter", END)

# Compile framework workflow graph execution context
research_graph = workflow.compile()