import json
from types import SimpleNamespace
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage

from src.application.utils.temp import Temp
from src.application.utils.format_util import FormatUtil
from src.application.services.tavily_service import TavilyService
from src.application.models.report_models import ReportState, ReportStateInput, ReportStateOutput
from src.application.config import configuration
from src.application.models.section_models import Queries, SectionOutputState, SectionState, Sections
from src.application.prompts.research_prompts import query_writer_instructions, report_planner_query_writer_instructions, report_planner_instructions

class ResearchAgent:        
    def __init__(self, model):
        section_builder = StateGraph(SectionState, output = SectionOutputState)
        section_builder.add_node("generate_queries", self.generate_queries)
        section_builder.add_node("search_web", self.search_web)
        section_builder.add_edge(START, "generate_queries")
        section_builder.add_edge("generate_queries", "search_web")
        section_builder.add_edge("search_web", END)    

        builder = StateGraph(ReportState, input=ReportStateInput, config_schema=configuration.Configuration)
        builder.add_node("generate_report_plan", self.generate_report_plan)
        builder.add_node("build_section_with_web_research", section_builder.compile())
        builder.add_node("gather_completed_sections", self.gather_completed_sections)
        builder.add_edge(START, "generate_report_plan")
        builder.add_conditional_edges("generate_report_plan", self.initiate_section_writing, ["build_section_with_web_research"])
        builder.add_edge("build_section_with_web_research", "gather_completed_sections")
        builder.add_edge("gather_completed_sections", END)
        self.graph = builder.compile() 
        self.llm_model = model

    def generate_queries(self, state: SectionState, config: RunnableConfig):
        """ Generate search queries for a repot section """

        section = state["section"]

        # configurable = configuration.Configuration.from_runnable_config(config)
        # number_of_queries = configurable.number_of_queries

        # structured_llm = self.llm_model.with_structured_output(Queries)

        # system_instructions = query_writer_instructions.format(section_topic=section.description, number_of_queries=number_of_queries)

        # queries = structured_llm.invoke([SystemMessage(content=system_instructions)] + [HumanMessage(content="Generate search queries on the provided topic.")])

        queries = Temp.get_queries()

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

        return {"source_str": source_str}


    async def generate_report_plan(self, state: ReportState, config: RunnableConfig):
        topic = state["topic"]

        # configurable = configuration.Configuration.from_runnable_config(config)
        # report_structure = configurable.report_structure
        # number_of_queries = configurable.number_of_queries
        # tavily_topic = configurable.tavily_topic
        # tavily_days = configurable.tavily_days

        # # Convert JSON object to string if necessary
        # if isinstance(report_structure, dict):
        #     report_structure = str(report_structure)
        
        # # Generate search query
        # structured_llm = self.llm_model.with_structured_output(Queries)

        # # Format system instructions
        # system_instructions_query = report_planner_query_writer_instructions.format(topic=topic, report_organization=report_structure, number_of_queries=number_of_queries)

        # # Generate queries
        # human_message = "Generate search queries that will help with planning the sections of the report."
        # results = structured_llm.invoke(
        #     [SystemMessage(content=system_instructions_query)]+[HumanMessage(content=human_message)])

        # # Web Search
        # query_list = [query.search_query for query in results.queries]

        # # Search Web
        # tavily_search = TavilyService()
        # search_docs = await tavily_search.tavily_search_async(
        #     search_queries=query_list, 
        #     tavily_topic=tavily_topic,
        #     tavily_days= tavily_days)


        # # Deduplicate and format sources
        # format_util = FormatUtil()
        # source_str = format_util.deduplicate_and_format_sources(
        #     search_response=search_docs, 
        #     max_tokens_per_source=1000, 
        #     include_raw_content=False)

        # # Format system instructions
        # system_instructions_sections = report_planner_instructions.format(topic=topic, report_organization=report_structure, context=source_str)

        # # Generate sections
        # structured_llm = self.llm_model.with_structured_output(Sections)
        # human_message = "Generate the sections of the report. Your response must include a 'sections' field containing a list of sections. \
        # Each section must have: name, description, plan, research, and content fields."
        # report_sections = structured_llm.invoke([SystemMessage(content=system_instructions_sections)]+[HumanMessage(content=human_message)])

        report_sections = Temp.get_report_sections()
        
        return {"sections": report_sections.sections}
    
    def initiate_section_writing(self, state: ReportState):
        """ This is the "map" step when we kick off web research for some sections of the report """    
            
        # Kick off section writing in parallel via Send() API for any sections that require research
        return [
            Send("build_section_with_web_research", {"section": s}) 
            for s in state["sections"] 
            if s.research
        ]
    
    def gather_completed_sections(state: ReportState):
        """ Gather completed sections from research and format them as context for writing the final sections """
        
        completed_sections = state["completed_sections"]

        # Format completed section to str to use as context for final sections
        completed_report_sections = FormatUtil.format_sections(completed_sections)

        return {"report_sections_from_research": completed_report_sections}
