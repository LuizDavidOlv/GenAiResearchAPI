import logging
from fastapi import APIRouter
from src.api.v1.models.rest_response import RestResponse
from src.application.service.summarization_service import SummarizationService

router = APIRouter(
    prefix="/summarize",
    tags = ["summarize"],
)

@router.post("/summarize-documents")
def summarize(request: str):
    data = SummarizationService.summarize(request)

    logging.debug("Returning response data at controller level")
    return RestResponse(data=data, message="Document Summarized")


@router.post("/write-essay")
def write_essay(request: str):
    data = SummarizationService.write_essay(request)

    logging.debug("Returning response data at controller level")
    return RestResponse(data=data, message="Essay Completed")