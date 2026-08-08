import os

from tavily import TavilyClient

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def web_search(query: str) -> str:
    """Search the web for information
    Args:
        query: the search query
    Returns:
        search results as text
    """

    client = TavilyClient(api_key=TAVILY_API_KEY)
    results = client.search(query, max_results=3)
    return "\n\n".join(f"{r['title']}: {r['content']}" for r in results['results'])