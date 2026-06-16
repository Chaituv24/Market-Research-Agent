import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import research_graph

app = FastAPI(
    title="Autonomous Multi-Agent Market Research Engine",
    version="1.1.0"
)

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic: str
    report: str

@app.post("/api/research", response_model=ResearchResponse)
async def run_market_research(request: ResearchRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Search parameters cannot be empty.")
        
    try:
        initial_state = {
            "topic": request.topic,
            "raw_data": "",
            "filtered_data": "",
            "final_report": ""
        }
        
        # Invoke the compiled execution graph synchronously
        final_state = research_graph.invoke(initial_state)
        
        return ResearchResponse(
            topic=final_state["topic"],
            report=final_state["final_report"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Graph Interruption: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)