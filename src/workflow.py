# src/workflow.py
from typing import TypedDict, Annotated, NotRequired
import operator
from langgraph.graph import StateGraph, END

from dotenv import load_dotenv
load_dotenv()
# Import your agents
from src.agents.research_agent import ResearchAgent
from src.agents.synthesis_agent import SynthesisAgent
from src.agents.quality_agent import QualityAgent
from src.agents.output_agent import OutputAgent

# Define state structure
class AgentState(TypedDict):
    query: str
    research_notes: str
    synthesis: str
    final_output: str
    approved: NotRequired[bool]
    quality_review: NotRequired[str]
    revision_feedback: NotRequired[str]

# Initialize agents
research_agent = ResearchAgent()
synthesis_agent = SynthesisAgent()
quality_agent = QualityAgent()
output_agent = OutputAgent()

async def research_node(state: AgentState) -> AgentState:
    """Research agent node"""
    print(f"🔍 Research Agent: Working on '{state['query']}'")
    
    result = await research_agent.research(state['query'], state)
    
    print(f"✅ Research Agent: Completed")
    print(f"📝 Research notes length: {len(result.get('research_notes', ''))} chars")
    
    return result

async def synthesis_node(state: AgentState) -> AgentState:
    """Synthesis agent node"""
    print(f"🧠 Synthesis Agent: Processing research")
    
    result = synthesis_agent.synthesize(state)
    
    print(f"✅ Synthesis Agent: Completed")
    print(f"📝 Synthesis length: {len(result.get('synthesis', ''))} chars")
    
    return result

async def quality_node(state: AgentState) -> AgentState:
    """Quality agent node"""
    print(f"🔍 Quality Agent: Reviewing synthesis")
    
    result = quality_agent.review(state)
    
    print(f"✅ Quality Agent: Completed")
    
    return result

async def output_node(state: AgentState) -> AgentState:
    """Output agent node"""
    print(f"📝 Output Agent: Formatting final response")
    
    result = output_agent.format_output(state)
    
    print(f"✅ Output Agent: Completed")
    
    return result

def should_continue(state: AgentState) -> str:
    """Decide whether to end or revise"""
    approved = state.get("approved", False)
    print(f"🔀 Router: approved={approved}, routing to {'OUTPUT' if approved else 'SYNTHESIS REVISION'}")
    
    if approved:
        return "end"
    else:
        return "revise"

# Build the workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("research", research_node)
workflow.add_node("synthesis", synthesis_node)
workflow.add_node("quality", quality_node)
workflow.add_node("output", output_node)

# Define edges (flow)
workflow.set_entry_point("research")
workflow.add_edge("research", "synthesis")
workflow.add_edge("synthesis", "quality")
workflow.add_conditional_edges(
    "quality",
    should_continue,
    {
        "end": "output",  # Go to output instead of END
        "revise": "synthesis"
    }
)

# Compile
app = workflow.compile()