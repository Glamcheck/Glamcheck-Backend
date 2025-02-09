from pydantic import Field, BaseModel

from .analysis_settings import AnalysisSettingsModel


class AnalysisRequestModel(BaseModel):
    composition: str = Field(
        max_length=10000,
        examples=[
            "Product: AQUA/WATER - SODIUM LAURETH SULFATE - COCO-GLUCOSIDE - GLYCERIN"
        ],
    )
    analysis_settings: AnalysisSettingsModel
