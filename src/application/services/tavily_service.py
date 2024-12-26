
import asyncio
from langsmith import traceable
from tavily import TavilyClient, AsyncTavilyClient


class TavilyService:
    def __init__(self):
        self.tavily_client= TavilyClient()
        self.tavily_async_client = AsyncTavilyClient()

    @traceable
    async def tavily_search_async(self, search_queries, tavily_topic, tavily_days):
        """
        Performs concurrent web searches using the Tavily API.

        Args:
            search_queries (List[SearchQuery]): List of search queries to process
            tavily_topic (str): Type of search to perform ('news' or 'general')
            tavily_days (int): Number of days to look back for news articles (only used when tavily_topic='news')

        Returns:
            List[dict]: List of search results from Tavily API, one per query

        Note:
            For news searches, each result will include articles from the last `tavily_days` days.
            For general searches, the time range is unrestricted.
        """
        
        search_tasks = []
        for query in search_queries:
            if tavily_topic == "news":
                search_tasks.append(
                    self.tavily_async_client.search(
                        query,
                        max_results=5,
                        include_raw_content=True,
                        topic="news",
                        days=tavily_days
                    )
                )
            else:
                search_tasks.append(
                    self.tavily_async_client.search(
                        query,
                        max_results=5,
                        include_raw_content=True,
                        topic="general"
                    )
                )

        # Execute all searches concurrently
        search_docs = await asyncio.gather(*search_tasks)

        return search_docs
    

    @traceable
    def tavily_search(self, query):
        """ Search the web using the Tavily API.
    
        Args:
            query (str): The search query to execute
            
        Returns:
            dict: Tavily search response containing:
                - results (list): List of search result dictionaries, each containing:
                    - title (str): Title of the search result
                    - url (str): URL of the search result
                    - content (str): Snippet/summary of the content
                    - raw_content (str): Full content of the page if available"""
        return self.tavily_client.search(query,max_results=5, include_raw_content=True)