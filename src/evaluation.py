from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from datasets import Dataset

def evaluate_research(query: str, response: str, contexts: list):
    """Evaluate RAG quality"""
    
    # Prepare dataset
    data = {
        "question": [query],
        "answer": [response],
        "contexts": [contexts]
    }
    dataset = Dataset.from_dict(data)
    
    # Run evaluation
    results = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision]
    )
    
    return results

# Test it
if __name__ == "__main__":
    query = "What is MCP?"
    response = "MCP is Model Context Protocol..."
    contexts = ["MCP is a protocol..."]
    
    scores = evaluate_research(query, response, contexts)
    print(scores)