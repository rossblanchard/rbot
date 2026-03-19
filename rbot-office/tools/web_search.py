"""
FILE: web_search.py
PURPOSE: Provides the AI swarm with live internet access via DuckDuckGo.
         This bypasses the need for Google Search API keys and provides 
         zero-configuration web scraping for real-time context.
INPUTS:  query (str): The search term to look up on the internet.
OUTPUTS: str: A formatted string containing the top 5 search results (Titles, URLs, and Snippets).
"""

from ddgs import DDGS

def search_web(query: str) -> str:
    """Searches DuckDuckGo and returns the top 5 results as a formatted string."""
    try:
        # Initialize the DuckDuckGo search client
        ddgs = DDGS()
        
        # Perform the search, limiting to the top 5 results to save LLM context tokens
        results = list(ddgs.text(query, max_results=5))
        
        if not results:
            return f"No web search results found for: '{query}'"
            
        # Format the results into a clean, readable string for the AI
        formatted_results = f"Web Search Results for '{query}':\n\n"
        for i, res in enumerate(results, 1):
            title = res.get('title', 'No Title')
            link = res.get('href', 'No URL')
            snippet = res.get('body', 'No snippet available.')
            
            formatted_results += f"{i}. {title}\nURL: {link}\nSnippet: {snippet}\n\n"
            
        return formatted_results

    except Exception as e:
        return f"Failed to search the web: {str(e)}"
