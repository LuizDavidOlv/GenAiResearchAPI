from langgraph.graph import StateGraph, START, END
from src.application.nodes.generate_reports_nodes import GenerateReportsNode
from src.application.nodes.section_writing_nodes import SectionWritingNodes
from src.application.nodes.web_search_nodes import WebSearchNodes
from src.application.models.report_models import ReportState, ReportStateInput, ReportStateOutput
from src.application.config import configuration
from src.application.models.section_models import SectionOutputState, SectionState

class ResearchAgent:        
    def __init__(self, model):
        web_search_nodes = WebSearchNodes(model)
        section_writing_nodes = SectionWritingNodes()
        generate_reports_nodes = GenerateReportsNode(model)

        section_builder = StateGraph(SectionState, output = SectionOutputState)
        section_builder.add_node("generate_queries", web_search_nodes.generate_queries) 
        section_builder.add_node("search_web", web_search_nodes.search_web)
        section_builder.add_node("write_section", web_search_nodes.write_section)
        section_builder.add_edge(START, "generate_queries")
        section_builder.add_edge("generate_queries", "search_web")
        section_builder.add_edge("search_web", "write_section")
        section_builder.add_edge("write_section", END)    

        builder = StateGraph(ReportState, input=ReportStateInput, output = ReportStateOutput, config_schema=configuration.Configuration)
        builder.add_node("generate_report_plan", generate_reports_nodes.generate_report_plan)
        builder.add_node("build_section_with_web_research", section_builder.compile())
        builder.add_node("gather_completed_sections", generate_reports_nodes.gather_completed_sections)
        builder.add_node("write_final_sections", generate_reports_nodes.write_final_sections)
        builder.add_node("compile_final_report", generate_reports_nodes.compile_final_report)
        builder.add_edge(START, "generate_report_plan")
        builder.add_conditional_edges("generate_report_plan", section_writing_nodes.initiate_section_writing, ["build_section_with_web_research"])
        builder.add_edge("build_section_with_web_research", "gather_completed_sections")
        builder.add_conditional_edges("gather_completed_sections", section_writing_nodes.initiate_final_section_writing, ["write_final_sections"])
        builder.add_edge("write_final_sections", "compile_final_report")
        builder.add_edge("compile_final_report", END)
        
        self.graph = builder.compile() 


   
