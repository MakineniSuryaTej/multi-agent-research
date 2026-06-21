# test_full_workflow.py
import asyncio
from src.workflow import app


from dotenv import load_dotenv
load_dotenv()

async def test_full_system():
    """Test the complete 4-agent workflow"""
    
    test_query = "What is Model Context Protocol (MCP) and why is it important?"
    
    print("=" * 70)
    print("🚀 TESTING FULL 4-AGENT WORKFLOW")
    print("=" * 70)
    print(f"\nQuery: {test_query}\n")
    
    result = await app.ainvoke({"query": test_query})
    
    print("\n" + "=" * 70)
    print("📊 FINAL OUTPUT")
    print("=" * 70)
    
    print(f"\n✅ Quality Review: {result.get('quality_review', 'N/A')[:200]}...")
    
    print(f"\n📝 FINAL FORMATTED OUTPUT:\n")
    print(result.get("final_output", "No output generated"))
    
    print("\n" + "=" * 70)
    print("✅ WORKFLOW COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_full_system())