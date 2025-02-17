from src.application.models.report_models import ReportState
from langgraph.constants import Send


class SectionWritingNodes:

    def initiate_section_writing(self, state: ReportState):
        """ This is the "map" step when we kick off web research for some sections of the report """    
            
        # Kick off section writing in parallel via Send() API for any sections that require research
        return [
            Send("build_section_with_web_research", {"section": s}) 
            for s in state["sections"] 
            if s.research
        ]
    
    def initiate_final_section_writing(self, state: ReportState):
        # Write any final sections using the Send API to parallelize the process
        
         return [
            Send("write_final_sections", {"section": s, "report_sections_from_research": state["report_sections_from_research"]}) 
            for s in state["sections"] 
            if not s.research
        ]