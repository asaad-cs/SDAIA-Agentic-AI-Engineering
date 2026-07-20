import os
from tavily import TavilyClient


def tavily_search(query: str) -> list[str]:
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    response = client.search(query=query, max_results=3)
    return [r["content"] for r in response.get("results", [])]
