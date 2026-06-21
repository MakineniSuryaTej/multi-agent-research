# test_workflow.py
from src.workflow import app

def test_basic_workflow():
    """Test the basic 2-agent workflow"""
    
    # Test query
    test_query = "What is Retrieval-Augmented Generation (RAG) in AI?"
    
    print("=" * 60)
    print("🚀 TESTING MULTI-AGENT WORKFLOW")
    print("=" * 60)
    print(f"\nQuery: {test_query}\n")
    
    # Run workflow
    try:
        result = app.invoke({"query": test_query})
        
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        
        print(f"\n🔍 RESEARCH NOTES:\n{result.get('research_notes', 'N/A')[:500]}...")
        
        print(f"\n🧠 SYNTHESIS:\n{result.get('synthesis', 'N/A')[:500]}...")
        
        print("\n✅ WORKFLOW COMPLETED SUCCESSFULLY!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_queries():
    """Test with multiple queries"""
    queries = [
        "What is Model Context Protocol (MCP)?",
        "Explain LangGraph in simple terms",
        "What are AI agents?"
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"Testing: {query}")
        print(f"{'='*60}")
        
        result = app.invoke({"query": query})
        print(f"✅ Result: {result.get('synthesis', 'N/A')[:200]}...")

if __name__ == "__main__":
    # Run basic test
    success = test_basic_workflow()
    
    if success:
        print("\n🎉 Basic test passed! Run test_multiple_queries() for more tests.")