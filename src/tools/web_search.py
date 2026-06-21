# src/tools/web_search.py
import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("web_search")

@mcp.tool()
async def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web for current information.
    Use this when you need up-to-date facts, current events, or specific data.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key:
        return "Error: TAVILY_API_KEY not set"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "max_results": max_results,
                "search_depth": "basic"
            }
        )
        
        data = response.json()
        
        # Format results
        results = []
        for result in data.get("results", []):
            results.append(f"Source: {result['url']}\nTitle: {result['title']}\nContent: {result['content'][:300]}...")
        
        return "\n\n---\n\n".join(results)

if __name__ == "__main__":
    # Test the tool
    import asyncio
    
    async def test():
        result = await web_search("What is LangGraph?")
        print(result)
    
    asyncio.run(test())