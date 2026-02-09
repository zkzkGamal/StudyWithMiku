from langchain_core.tools import tool
import ddgs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@tool
def duckduckgo_search(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo"""
    try:
        results = []
        with ddgs.DDGS() as search:
            for r in search.text(query, max_results=max_results):
                logger.info(f"Result: {r['title']}\n{r['body']}\nURL: {r['href']}")
                results.append(
                    f"{r['title']}\n{r['body']}\nURL: {r['href']}"
                )

        return "\n\n".join(results)
    except Exception as e:
        logger.error(f"[TOOL] DuckDuckGo search error: {e}")
        return f"Error searching the web: {e}"
