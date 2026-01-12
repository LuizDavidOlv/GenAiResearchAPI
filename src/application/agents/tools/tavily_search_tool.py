from datetime import datetime

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.tools import InjectedToolArg, tool
from tavily import TavilyClient
from typing_extensions import Annotated, List, Literal

from src.application.agents.deep_research_agent.states.researcher_state import Summary
from src.application.utils.date_util import get_today_str


class TavilySearchTool:
    def __init__(self, llm_model: str):
        self.web_seach_summarization_model = init_chat_model(model=llm_model)
        self.tavily_client = TavilyClient()

    @tool(parse_docttring=True)
    def tavily_search(
        self,
        query: str,
        max_results: Annotated[int, InjectedToolArg] = 3,
        topic: Annotated[
            Literal["general", "news", "finance"], InjectedToolArg
        ] = "general",
    ) -> str:
        """
        Fetch results from Tavily search API with content summarizaiton.

        Args:
            query: A single search query to execute
            max_results: Maximum number of results to return
            topic: Topic to filter results by ('general', 'news', 'finance')

        Returns:
            Formatted string of search results with summaries
        """
        search_results = self.tavily_search_multiple(
            [query],
            max_results=max_results,
            topic=topic,
            include_raw_content=True,
        )

        unique_results = self.deduplicate_search_results(search_results)
        summarized_results = self.process_search_results(unique_results)

        formated_result = self.format_search_output(summarized_results)
        return formated_result

    def tavily_search_multiple(
        self,
        search_queries: List[str],
        max_results: int = 3,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = True,
    ) -> List[dict]:
        """Perform search using Tavily API for multiple queries.

        Args:
            search_queries: List of search queries to execute
            max_results: Maximum number of results per query
            topic: Topic filter for search results
            include_raw_content: Whether to include raw webpage content

        Returns:
            List of search result dictionaries
        """
        # Execute searches sequentially. Note: yon can use AsyncTavilyClient to parallelize this step.
        search_docs = []
        for query in search_queries:
            result = self.tavily_client.search(
                query,
                max_results=max_results,
                include_raw_content=include_raw_content,
                topic=topic,
            )
            search_docs.append(result)

        return search_docs

    def deduplicate_search_results(self, search_results: List[dict]) -> dict:
        """Deduplicate search results by URL to avoid processing duplicate content.

        Args:
            search_results: List of search result dictionaries

        Returns:
            Dictionary mapping URLs to unique results
        """
        unique_results = {}

        for response in search_results:
            for result in response["results"]:
                url = result["url"]
                if url not in unique_results:
                    unique_results[url] = result

        return unique_results

    def summarize_webpage_content(self, webpage_content: str) -> str:
        """Summarize webpage content using the configured summarization model.

        Args:
            webpage_content: Raw webpage content to summarize

        Returns:
            Formatted summary with key excerpts
        """
        try:
            # Set up structured output model for summarization
            structured_model = (
                self.web_seach_summarization_model.with_structured_output(Summary)
            )

            # Generate summary
            summarize_webpage_prompt = self.get_webpage_summarization_prompt()
            summary = structured_model.invoke(
                [
                    HumanMessage(
                        content=summarize_webpage_prompt.format(
                            webpage_content=webpage_content, date=get_today_str()
                        )
                    )
                ]
            )

            # Format summary with clear structure
            formatted_summary = (
                f"<summary>\n{summary.summary}\n</summary>\n\n"
                f"<key_excerpts>\n{summary.key_excerpts}\n</key_excerpts>"
            )

            return formatted_summary

        except Exception as e:
            print(f"Failed to summarize webpage: {str(e)}")
            return (
                webpage_content[:1000] + "..."
                if len(webpage_content) > 1000
                else webpage_content
            )

    def process_search_results(self, unique_results: dict) -> dict:
        """Process search results by summarizing content where available.

        Args:
            unique_results: Dictionary of unique search results

        Returns:
            Dictionary of processed results with summaries
        """
        summarized_results = {}

        for url, result in unique_results.items():
            # Use existing content if no raw content for summarization
            if not result.get("raw_content"):
                content = result["content"]
            else:
                # Summarize raw content for better processing
                content = self.summarize_webpage_content(result["raw_content"])

            summarized_results[url] = {"title": result["title"], "content": content}

        return summarized_results

    def format_search_output(self, summarized_results: dict) -> str:
        """Format search results into a well-structured string output.

        Args:
            summarized_results: Dictionary of processed search results

        Returns:
            Formatted string of search results with clear source separation
        """
        if not summarized_results:
            return "No valid search results found. Please try different search queries or use a different search API."

        formatted_output = "Search results: \n\n"

        for i, (url, result) in enumerate(summarized_results.items(), 1):
            formatted_output += f"\n\n--- SOURCE {i}: {result['title']} ---\n"
            formatted_output += f"URL: {url}\n\n"
            formatted_output += f"SUMMARY:\n{result['content']}\n\n"
            formatted_output += "-" * 80 + "\n"

        return formatted_output

    def get_webpage_summarization_prompt(self):
        summarize_webpage_prompt = """You are tasked with summarizing the raw content of a webpage retrieved from a web search. Your goal is to create a summary that preserves the most important information from the original web page. This summary will be used by a downstream research agent, so it's crucial to maintain the key details without losing essential information.

Here is the raw content of the webpage:

<webpage_content>
{webpage_content}
</webpage_content>

Please follow these guidelines to create your summary:

1. Identify and preserve the main topic or purpose of the webpage.
2. Retain key facts, statistics, and data points that are central to the content's message.
3. Keep important quotes from credible sources or experts.
4. Maintain the chronological order of events if the content is time-sensitive or historical.
5. Preserve any lists or step-by-step instructions if present.
6. Include relevant dates, names, and locations that are crucial to understanding the content.
7. Summarize lengthy explanations while keeping the core message intact.

When handling different types of content:

- For news articles: Focus on the who, what, when, where, why, and how.
- For scientific content: Preserve methodology, results, and conclusions.
- For opinion pieces: Maintain the main arguments and supporting points.
- For product pages: Keep key features, specifications, and unique selling points.

Your summary should be significantly shorter than the original content but comprehensive enough to stand alone as a source of information. Aim for about 25-30 percent of the original length, unless the content is already concise.

Present your summary in the following format:

```
{{
   "summary": "Your summary here, structured with appropriate paragraphs or bullet points as needed",
   "key_excerpts": "First important quote or excerpt, Second important quote or excerpt, Third important quote or excerpt, ...Add more excerpts as needed, up to a maximum of 5"
}}
```

Here are two examples of good summaries:

Example 1 (for a news article):
```json
{{
   "summary": "On July 15, 2023, NASA successfully launched the Artemis II mission from Kennedy Space Center. This marks the first crewed mission to the Moon since Apollo 17 in 1972. The four-person crew, led by Commander Jane Smith, will orbit the Moon for 10 days before returning to Earth. This mission is a crucial step in NASA's plans to establish a permanent human presence on the Moon by 2030.",
   "key_excerpts": "Artemis II represents a new era in space exploration, said NASA Administrator John Doe. The mission will test critical systems for future long-duration stays on the Moon, explained Lead Engineer Sarah Johnson. We're not just going back to the Moon, we're going forward to the Moon, Commander Jane Smith stated during the pre-launch press conference."
}}
```

Example 2 (for a scientific article):
```json
{{
   "summary": "A new study published in Nature Climate Change reveals that global sea levels are rising faster than previously thought. Researchers analyzed satellite data from 1993 to 2022 and found that the rate of sea-level rise has accelerated by 0.08 mm/year² over the past three decades. This acceleration is primarily attributed to melting ice sheets in Greenland and Antarctica. The study projects that if current trends continue, global sea levels could rise by up to 2 meters by 2100, posing significant risks to coastal communities worldwide.",
   "key_excerpts": "Our findings indicate a clear acceleration in sea-level rise, which has significant implications for coastal planning and adaptation strategies, lead author Dr. Emily Brown stated. The rate of ice sheet melt in Greenland and Antarctica has tripled since the 1990s, the study reports. Without immediate and substantial reductions in greenhouse gas emissions, we are looking at potentially catastrophic sea-level rise by the end of this century, warned co-author Professor Michael Green."  
}}
```

Remember, your goal is to create a summary that can be easily understood and utilized by a downstream research agent while preserving the most critical information from the original webpage.

Today's date is {date}.
"""

        return summarize_webpage_prompt
