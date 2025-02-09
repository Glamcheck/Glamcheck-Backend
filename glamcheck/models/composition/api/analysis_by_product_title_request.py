from pydantic import Field, BaseModel

from .analysis_settings import AnalysisSettingsModel


class AnalysisByProductTitleRequestModel(BaseModel):
    product_title: str = Field(max_length=1000, examples=["Product title"])
    analysis_settings: AnalysisSettingsModel
