from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

class OutputAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-haiku-4-5")
    
    def format_output(self, state: dict) -> dict:
        """Format final output"""
        print(f"📝 Output Agent: Formatting final response")
        
        synthesis = state.get("synthesis", "")
        sources = state.get("sources", "")
        
        messages = [
            SystemMessage(content="""Format the following research into a clear, 
            structured response with:
            - Executive Summary
            - Key Points
            - Sources
            
            Make it professional and easy to read."""),
            
            HumanMessage(content=f"""Synthesis:
            {synthesis}
            
            Sources:
            {sources}
            
            Format this nicely.""")
        ]
        
        response = self.llm.invoke(messages)
        state["final_output"] = response.content
        
        print(f"✅ Output formatted: {len(response.content)} chars")
        
        return state