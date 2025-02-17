from src.application.config import configuration
from src.application.models.section_models import SectionState
from langchain_core.runnables import RunnableConfig
from src.application.services.tavily_service import TavilyService
from src.application.utils.format_util import FormatUtil
from src.application.models.section_models import Queries, SectionState
from src.application.prompts.research_prompts import query_writer_instructions, section_writer_instructions
from langchain_core.messages import HumanMessage, SystemMessage


class WebSearchNodes:
    def __init__(self, model):
        self.llm_model = model
    
    def generate_queries(self, state: SectionState, config: RunnableConfig):
            """ Generate search queries for a repot section """

            section = state["section"]

            configurable = configuration.Configuration.from_runnable_config(config)
            number_of_queries = configurable.number_of_queries

            structured_llm = self.llm_model.with_structured_output(Queries)

            system_instructions = query_writer_instructions.format(section_topic=section.description, number_of_queries=number_of_queries)

            queries = structured_llm.invoke([SystemMessage(content=system_instructions)] + [HumanMessage(content="Generate search queries on the provided topic.")])

            return {"search_queries": queries.queries}
    

    async def search_web(self, state: SectionState, config= RunnableConfig):
        """ Search the web for each query, then return a list of raw sources and a formatted string of sources"""

        search_queries = state['search_queries']


        configurable = configuration.Configuration.from_runnable_config(config)
        tavily_topic = configurable.tavily_topic
        tavily_days = configurable.tavily_days

        query_list = [query.search_query for query in search_queries]
        search_docs = await TavilyService().tavily_search_async(query_list, tavily_topic, tavily_days)

        source_str = FormatUtil.deduplicate_and_format_sources(search_docs, max_tokens_per_source=5000, include_raw_content=True)

        #source_str = Temp2.get_source_str()

        return {"source_str": source_str}
    

    def write_section(self, state: SectionState):
        """ write a section of the report """
        section = state["section"]
        source_str = state["source_str"]

        system_instructions = section_writer_instructions.format(section_title=section.name, section_topic=section.description, context=source_str)

        section_content = self.llm_model.invoke([SystemMessage(content=system_instructions)]+[HumanMessage(content="Generate a report section based on the provided sources.")])
        section.content = section_content.content

        return {"completed_sections": [section]}