from pydantic import BaseModel

from .range_additional_property import RangeAdditionalPropertyModel
from .range_cosmetic_property import RangeCosmeticPropertyModel
from glamcheck.models.composition.domain import NaturalnessType, DangerFactorModel


class AnalysisResultModel(BaseModel):
    naturalness: NaturalnessType
    danger_factor: DangerFactorModel
    skin_types: list[str]
    cosmetic_properties: list[RangeCosmeticPropertyModel]
    additional_properties: list[RangeAdditionalPropertyModel]
