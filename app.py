import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from pydantic import BaseModel
from graph import research_graph

app = FastAPI(
    title="Autonomous Multi-Agent Market Research Engine",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic: str
    report: str

def run_research_ui(topic):
    if not topic.strip():
        return "Please enter a valid research topic first."
    
    try:
        initial_state = {
            "topic": topic,
            "raw_data": "",
            "filtered_data": "",
            "final_report": ""
        }
        final_state = research_graph.invoke(initial_state)
        return final_state.get("final_report", "No report text returned by agents.")
    except Exception as e:
        return f"Internal Graph Interruption: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# AI Multi-Agent Market Research Engine")
    gr.Markdown("Enter a topic below to activate the LangGraph multi-agent orchestration pipeline.")
    
    with gr.Row():
        topic_input = gr.Textbox(
            label="Research Topic / Company Name", 
            placeholder="e.g., Electric Vehicles market growth in India",
            lines=1
        )
    
    submit_btn = gr.Button("Launch Research Agents", variant="primary")
    
    gr.Markdown("### Final Compiled Market Report")
    output_report = gr.Markdown(value="*Your generated market report will appear here...*")
    
    submit_btn.click(
        fn=run_research_ui, 
        inputs=topic_input, 
        outputs=output_report
    )

app = gr.mount_gradio_app(app, demo, path="/")

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
        final_state = research_graph.invoke(initial_state)
        return ResearchResponse(
            topic=final_state["topic"],
            report=final_state["final_report"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Graph Interruption: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)