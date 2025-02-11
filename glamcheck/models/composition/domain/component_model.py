from typing import Optional

from pydantic import BaseModel

from .additional_property_model import AdditionalPropertyModel
from .cosmetic_property_model import CosmeticPropertyModel
from .danger_factor_model import DangerFactorModel
from .input_percentage_model import InputPercentageModel
from .naturalness_type import NaturalnessType


class ComponentModel(BaseModel):
    traditional_title: str
    latin_title: str
    inci_title: str
    url: str
    categories: list[str]
    cosmetic_properties: list[CosmeticPropertyModel]
    additional_properties: list[AdditionalPropertyModel]
    aliases: list[str]
    skin_types: list[str]
    recommended_input_percentage: Optional[InputPercentageModel]
    danger_factor: Optional[DangerFactorModel]
    naturalness: Optional[NaturalnessType]
    hlb_value: Optional[float]
    comment: Optional[str]
