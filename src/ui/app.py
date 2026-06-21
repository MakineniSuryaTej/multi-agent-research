import streamlit as st
import asyncio
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..", "..")
sys.path.insert(0, project_root)

from src.workflow import app

st.set_page_config(page_title="Multi-Agent Research Assistant", layout="wide")

st.title("🔍 Multi-Agent Research Assistant")
st.markdown("Powered by LangGraph, MCP, and Claude")

# Input
query = st.text_input("Enter your research question:", 
                      placeholder="What is Model Context Protocol?")

# Run button
if st.button("Research", type="primary"):
    with st.spinner("Agents working..."):
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run workflow
        result = asyncio.run(app.ainvoke({"query": query}))
        
        progress_bar.progress(100)
        
    # Display results in tabs
    tab1, tab2, tab3 = st.tabs(["Final Output", "Research Process", "Quality Review"])
    
    with tab1:
        st.markdown(result.get("final_output", "No output"))
    
    with tab2:
        st.subheader("Research Notes")
        st.markdown(result.get("research_notes", "N/A")[:1000] + "...")
        
        st.subheader("Synthesis")
        st.markdown(result.get("synthesis", "N/A")[:1000] + "...")
    
    with tab3:
        st.markdown(result.get("quality_review", "N/A"))

# Sidebar
st.sidebar.markdown("""
### About
This system uses:
- **Research Agent**: Web search & data gathering
- **Synthesis Agent**: Information synthesis  
- **Quality Agent**: Accuracy review
- **Output Agent**: Professional formatting

Built with LangGraph + MCP + Claude
""")