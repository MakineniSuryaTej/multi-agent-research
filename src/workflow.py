# src/workflow.py
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END

from dotenv import load_dotenv
load_dotenv()
# Import your agents
from src.agents.research_agent import ResearchAgent
from src.agents.synthesis_agent import SynthesisAgent

# Define state structure
class AgentState(TypedDict):
    query: str
    research_notes: str
    synthesis: str
    final_output: str

# Initialize agents
research_agent = ResearchAgent()
synthesis_agent = SynthesisAgent()

def research_node(state: AgentState) -> AgentState:
    """Research agent node"""
    print(f"🔍 Research Agent: Working on '{state['query']}'")
    
    result = research_agent.research(state['query'], state)
    
    print(f"✅ Research Agent: Completed")
    print(f"📝 Research notes length: {len(result.get('research_notes', ''))} chars")
    
    return result

def synthesis_node(state: AgentState) -> AgentState:
    """Synthesis agent node"""
    print(f"🧠 Synthesis Agent: Processing research")
    
    result = synthesis_agent.synthesize(state)
    
    print(f"✅ Synthesis Agent: Completed")
    print(f"📝 Synthesis length: {len(result.get('synthesis', ''))} chars")
    
    return result

# Build the workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("research", research_node)
workflow.add_node("synthesis", synthesis_node)

# Define edges (flow)
workflow.set_entry_point("research")
workflow.add_edge("research", "synthesis")
workflow.add_edge("synthesis", END)

# Compile
app = workflow.compile()