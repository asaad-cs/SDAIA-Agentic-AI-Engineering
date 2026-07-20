from langgraph.graph import StateGraph, START, END
from state import ResearchState
from nodes import generate_query, web_search, evaluate_results, generate_report


def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("generate_query", generate_query)
    graph.add_node("web_search", web_search)
    graph.add_node("evaluate_results", evaluate_results)
    graph.add_node("generate_report", generate_report)

    graph.add_edge(START, "generate_query")
    graph.add_edge("generate_query", "web_search")
    graph.add_edge("web_search", "evaluate_results")

    # Loop back to search again, or move on to the report
    graph.add_conditional_edges(
        "evaluate_results",
        lambda s: "generate_report" if s.get("enough_info") else "generate_query",
    )

    graph.add_edge("generate_report", END)

    return graph.compile()
