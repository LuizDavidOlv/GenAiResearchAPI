from fastapi import APIRouter, status

from src.api.v1.models.health_response import HealthResponse
from src.api.v1.models.rest_response import RestResponse

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=RestResponse[HealthResponse],
)
def health():
    return RestResponse(
        data=HealthResponse(status="up"),
        message="API is up and running.",
    )
