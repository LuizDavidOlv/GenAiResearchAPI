from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage

from src.application.utils.format_util import FormatUtil
from src.application.services.tavily_service import TavilyService
from src.application.models.report_models import ReportState
from src.application.config import configuration
from src.application.models.section_models import Queries, SectionState, Sections
from src.application.prompts.research_prompts import report_planner_query_writer_instructions, report_planner_instructions, final_section_writer_instructions


class GenerateReportsNode:
    def __init__(self, model):
        self.llm_model = model
        
    async def generate_report_plan(self, state: ReportState, config: RunnableConfig):
        topic = state["topic"]

        configurable = configuration.Configuration.from_runnable_config(config)
        report_structure = configurable.report_structure
        number_of_queries = configurable.number_of_queries
        tavily_topic = configurable.tavily_topic
        tavily_days = configurable.tavily_days

        # Convert JSON object to string if necessary
        if isinstance(report_structure, dict):
            report_structure = str(report_structure)
        
        # Generate search query
        structured_llm = self.llm_model.with_structured_output(Queries)

        # Format system instructions
        system_instructions_query = report_planner_query_writer_instructions.format(topic=topic, report_organization=report_structure, number_of_queries=number_of_queries)

        # Generate queries
        human_message = "Generate search queries that will help with planning the sections of the report."
        results = structured_llm.invoke(
            [SystemMessage(content=system_instructions_query)]+[HumanMessage(content=human_message)])

        # Web Search
        query_list = [query.search_query for query in results.queries]

        # Search Web
        tavily_search = TavilyService()
        search_docs = await tavily_search.tavily_search_async(
            search_queries=query_list, 
            tavily_topic=tavily_topic,
            tavily_days= tavily_days)


        # Deduplicate and format sources
        format_util = FormatUtil()
        source_str = format_util.deduplicate_and_format_sources(
            search_response=search_docs, 
            max_tokens_per_source=1000, 
            include_raw_content=False)

        # Format system instructions
        system_instructions_sections = report_planner_instructions.format(topic=topic, report_organization=report_structure, context=source_str)

        # Generate sections
        structured_llm = self.llm_model.with_structured_output(Sections)
        human_message = "Generate the sections of the report. Your response must include a 'sections' field containing a list of sections. \
        Each section must have: name, description, plan, research, and content fields."
        report_sections = structured_llm.invoke([SystemMessage(content=system_instructions_sections)]+[HumanMessage(content=human_message)])

        #report_sections = Temp.get_report_sections()
        
        return {"sections": report_sections.sections}
    

    def gather_completed_sections(self, state: ReportState):
        """ Gather completed sections from research and format them as context for writing the final sections """
        
        completed_sections = state["completed_sections"]

        # Format completed section to str to use as context for final sections
        completed_report_sections = FormatUtil.format_sections(completed_sections)

        return {"report_sections_from_research": completed_report_sections}


    def write_final_sections(self, state: SectionState):
        """ Write final sections of the report, which do not require web search and use the completed sections as context """

        section = state["section"]
        completed_report_sections = state["report_sections_from_research"]

        system_instructions = final_section_writer_instructions.format(section_title=section.name, section_topic=section.description, context=completed_report_sections)

        section_content = self.llm_model.invoke([SystemMessage(content=system_instructions)]+[HumanMessage(content="Generate a report section based on the provided sources.")])
        section.content = section_content.content

        return {"completed_sections": [section]}

    def compile_final_report(self, state: ReportState):
        sections = state["sections"]
        completed_sections = {s.name: s.content for s in state["completed_sections"]}

        for section in sections:
            section.content = completed_sections[section.name]

        all_sections = "\n\n".join([s.content for s in sections])

        return {"final_report": all_sections}