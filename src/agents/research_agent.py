# src/agents/research_agent.py
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool
import httpx
import os

class ResearchAgent:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-haiku-4-5")
    
    async def web_search(self, query: str) -> str:
        """Search the web using Tavily"""
        api_key = os.getenv("TAVILY_API_KEY")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": api_key,
                    "query": query,
                    "max_results": 3
                }
            )
            data = response.json()
            
            results = []
            for result in data.get("results", []):
                results.append(f"{result['title']}: {result['content'][:200]}")
            
            return "\n".join(results)
    
    async def research(self, query: str, state: dict) -> dict:
        """Research with real web search"""
        print(f"🔍 Research Agent: Searching web for '{query}'")
        
        # Search web
        search_results = await self.web_search(query)
        
        print(f"📚 Found {len(search_results)} characters of search results")
        
        # Use LLM to synthesize search results
        messages = [
            SystemMessage(content="""You are a research agent. 
            Analyze the provided search results and extract key information.
            Focus on facts, data, and authoritative sources.
            Cite specific sources when possible."""),
            
            HumanMessage(content=f"""Query: {query}
            
            Search Results:
            {search_results}
            
            Provide a comprehensive research summary with key findings and sources.""")
        ]
        
        response = self.llm.invoke(messages)
        
        # Update state
        state["research_notes"] = response.content
        state["sources"] = search_results[:500]  # Truncate for state
        
        print(f"✅ Research complete: {len(response.content)} chars")
        
        return state