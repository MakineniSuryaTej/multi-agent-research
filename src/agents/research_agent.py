from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

class ResearchAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-sonnet-4-5")
    
    def research(self, query: str, state: dict) -> dict:
        """Research a topic and return findings"""
        messages = [
            SystemMessage(content="You are a research agent. Find relevant information about the user's query."),
            HumanMessage(content=f"Research this topic: {query}")
        ]
        
        response = self.llm.invoke(messages)
        
        # Update state with research findings
        state["research_notes"] = response.content
        state["sources"] = []  # Will add real sources later
        
        return state