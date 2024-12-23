import logging
from fastapi import APIRouter
from src.api.v1.models.research_request import ResearchRequest
from src.api.v1.models.rest_response import RestResponse
from src.application.services.research_service import ResearchService

router = APIRouter(
    prefix="/research",
    tags = ["research"],
)

@router.post("/research-topic")
def research_topic(request: ResearchRequest):
    data = ResearchService.research(request)

    logging.debug("Returning response data at controller level")
    return RestResponse(data=data, message="Document Summarized")


# @router.post("/write-essay")
# def write_essay(request: str):
#     data = ResearchService.write_essay(request)

#     logging.debug("Returning response data at controller level")
#     return RestResponse(data=data, message="Essay Completed")