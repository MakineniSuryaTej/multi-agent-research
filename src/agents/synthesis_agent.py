from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

class SynthesisAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4-5")
    
    def synthesize(self, state: dict) -> dict:
        """Synthesize research into coherent summary"""
        research = state.get("research_notes", "")
        
        messages = [
            SystemMessage(content="Synthesize the research into a clear, structured summary."),
            HumanMessage(content=f"Synthesize this research: {research}")
        ]
        
        response = self.llm.invoke(messages)
        state["synthesis"] = response.content
        
        return state