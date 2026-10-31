"""Main entry point"""
from agent.agent import Agent


agent = Agent()
initial_state = {  #2
    "user_question": " What can you tell me about Kyriakos Mitsotakis?",
    "assistant_info": None,
    "search_queries": None,
    "search_results": None,
    "search_summaries": None,
    "research_summary": None,
    "final_report": None,
    "used_fallback_search": False,
    "relevance_evaluation": None,
    "should_regenerate_queries": None,
    "iteration_count": 0
}

agent.create_node()
agent.connect_edges()

app = agent.compile_graph()

result = app.invoke(initial_state)
print(result)