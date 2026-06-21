from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

class QualityAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-haiku-4-5")
    
    def review(self, state: dict) -> dict:
        """Review synthesis for quality"""
        print(f"✅ Quality Agent: Reviewing synthesis")
        
        query = state.get("query", "")
        synthesis = state.get("synthesis", "")
        research = state.get("research_notes", "")
        
        messages = [
            SystemMessage(content="""You are a quality review agent.
            Evaluate if the synthesis accurately reflects the research.
            Check for:
            1. Accuracy - Does it match the research?
            2. Completeness - Did it address the query?
            3. Clarity - Is it well-written?
            
            Respond with:
            APPROVED: [brief reason]
            or
            NEEDS_REVISION: [specific feedback]"""),
            
            HumanMessage(content=f"""Original Query: {query}
            
            Research Notes:
            {research[:1000]}
            
            Synthesis:
            {synthesis}
            
            Provide your quality assessment.""")
        ]
        
        response = self.llm.invoke(messages)
        assessment = response.content
        
        state["quality_review"] = assessment
        
        # Determine if approved
        if "APPROVED" in assessment.upper():
            state["approved"] = True
            print(f"✅ Quality Agent: APPROVED")
        else:
            state["approved"] = False
            state["revision_feedback"] = assessment
            print(f"⚠️ Quality Agent: NEEDS_REVISION")
        
        return state