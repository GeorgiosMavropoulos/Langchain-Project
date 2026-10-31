"""Creates the nodes and the edges to run the agent"""
from node_functions.node_functions import Nodes
from langgraph.graph import StateGraph, END
from type_dicts.type_dict import ResearchState

nodes = Nodes()

class Agent:
    def __init__(self):
    
     self.graph = StateGraph(ResearchState)


    #created the node
    def create_node(self):
       """ Creates the nodes using the methods from Node functions"""
       self.graph.add_node("select_assistant",nodes.select_assistant) 
       
       self.graph.add_node("generate_search_queries", nodes.generate_search_queries)   
       self.graph.add_node("search_web",  nodes.search_web)  
       self.graph.add_node('scrap_text',nodes.scrap_web)
       self.graph.add_node('generate_summary',nodes.generate_summary)
       self.graph.add_node('generate_report',nodes.research_report)


    def route_based_on_relevance(self,state):  
        """Create the routes based on the state"""
        iteration_count = state.get("iteration_count", 0) + 1
        state["iteration_count"] = iteration_count

        if iteration_count >= 3:
            return "generate_report"
        if state.get("should_regenerate_queries", False):
            return "generate_search_queries"
        return "generate_report"

    def connect_edges(self):
       self.graph.add_edge("select_assistant", "generate_search_queries")
       self.graph.add_edge("generate_search_queries",  "search_web")  
       self.graph.add_edge("search_web","scrap_text")
       self.graph.add_edge("scrap_text", "generate_summary")   #4
        #4
       self.graph.add_edge("generate_report", END)

       self.graph.add_conditional_edges(
        "generate_summary",
        self.route_based_on_relevance,
        {
            "generate_search_queries": "generate_search_queries",
            "generate_report": "generate_report"
        }
    )
       #set an entrypoint
       self.graph.set_entry_point("select_assistant")
       self.app = self.graph.compile()



    def compile_graph(self):

        self.app = self.graph.compile()

        return self.app

