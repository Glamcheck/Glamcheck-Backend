from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from glamcheck.models.common import DetailResponseModel
from glamcheck.models.composition.api import (
    AnalysisRequestModel,
    AnalysisByProductTitleRequestModel,
    AnalysisResponseModel
)

composition_router = APIRouter(tags=["composition"], prefix="/composition")


@composition_router.post(
    path="/analyze",
    operation_id="analyze",
    responses={
        HTTP_200_OK: {
            "description": "Composition is analyzed",
            "model": AnalysisResponseModel,
        },
        HTTP_400_BAD_REQUEST: {
            "description": "Invalid composition",
            "model": DetailResponseModel,
        },
    },
)
async def analyze(request_model: AnalysisRequestModel):
    return {"Hello": "World"}


@composition_router.post(
    path="/analyze-by-title",
    operation_id="analyzeByTitle",
    responses={
        HTTP_200_OK: {
            "description": "Composition is analyzed",
            "model": AnalysisResponseModel,
        },
        HTTP_404_NOT_FOUND: {
            "description": "Product not found",
            "model": DetailResponseModel,
        },
    },
)
async def analyze(request_model: AnalysisByProductTitleRequestModel):
    return {"Hello": "World"}
