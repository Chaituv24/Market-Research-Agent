import streamlit as st
import requests

# 1. Configure the page layout
st.set_page_config(
    page_title="AI Market Research Engine", 
    layout="centered"
)

# Title and Sub-header
st.title("AI Multi-Agent Market Research Engine")
st.write("Enter a research topic below to activate the LangGraph multi-agent orchestration pipeline.")

# 2. Input container field for the user
topic = st.text_input(
    label="Research Topic / Company Name", 
    placeholder="e.g., Electric Vehicles market growth in India"
)

# 3. Action execution handler button
if st.button("Launch Research Agents", type="primary"):
    # Input validation block
    if not topic.strip():
        st.warning("Please enter a valid topic first!")
    else:
        # Visual loading spinner while waiting for the network response from Render
        with st.spinner("Agents are searching, analyzing data, and updating vector storage..."):
            try:
                # Points directly to your active live hosted backend API endpoint
                API_URL = "https://market-research-agent-2xdb.onrender.com/start-research"
                
                # Payload matching your FastAPI Pydantic request body schema
                payload = {"topic": topic}
                
                # Execute the network POST request
                response = requests.post(API_URL, json=payload)
                
                # Verify successful server loop execution (Status 200)
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Research Generation Complete!")
                    
                    # 4. Collapsible section tracking LangGraph Agent Steps
                    with st.expander("View Agent Execution Logs"):
                        steps = result.get("execution_steps", [])
                        if steps:
                            for step in steps:
                                st.caption(f"Success: {step}")
                        else:
                            st.caption("Scraper node completed -> Analyst node compiled -> DB synchronized.")
                    
                    # 5. Output Container displaying the main research report document
                    st.subheader("Final Compiled Market Report")
                    
                    # Renders Markdown syntax returned from your Groq LLM node
                    report_content = result.get("generated_report", "") or result.get("itinerary", "")
                    if report_content:
                        st.markdown(report_content)
                    else:
                        st.info("The agents ran successfully, but returned an empty report asset body.")
                        
                else:
                    st.error(f"Backend Engine Error: Received status code {response.status_code} from Render server.")
                    
            except Exception as e:
                st.error(f"Failed to establish network connection to the live Render host: {str(e)}")