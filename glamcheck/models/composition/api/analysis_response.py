from typing import Optional

from pydantic import BaseModel

from .analysis_result import AnalysisResultModel


class AnalysisResponseModel(BaseModel):
    result: Optional[AnalysisResultModel]
    not_found_components: list[str]
