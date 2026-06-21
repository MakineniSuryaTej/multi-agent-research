# test_tools.py
import asyncio
from src.agents.research_agent import ResearchAgent

from dotenv import load_dotenv
load_dotenv()

async def test_web_search():
    agent = ResearchAgent()
    
    result = await agent.research(
        "What are the latest developments in AI agents 2025?",
        {"query": "test", "research_notes": "", "synthesis": "", "final_output": ""}
    )
    
    print("RESEARCH NOTES:")
    print(result["research_notes"][:1000])
    print("\nSOURCES:")
    print(result["sources"][:500])

if __name__ == "__main__":
    asyncio.run(test_web_search())