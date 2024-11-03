from typing import Optional

from pydantic import BaseModel

from additional_property import AdditionalProperty
from cosmetic_property import CosmeticProperty
from danger_factor import DangerFactor
from input_percentage import InputPercentage
from naturalness import Naturalness


class Component(BaseModel):
    traditional_title: str  # Добавить ограничения на длину?
    latin_title: str  # Добавить ограничения на длину?
    inci_title: str  # Добавить ограничения на длину?
    url: str  # Добавить ограничения на длину?
    categories: list[str]  # Добавить ограничения на длину?
    cosmetic_properties: list[CosmeticProperty]
    additional_properties: list[AdditionalProperty]
    aliases: list[str]  # Добавить ограничения на длину?
    skin_types: list[str]
    recommended_input_percentage: Optional[InputPercentage]
    danger_factor: Optional[DangerFactor]
    naturalness: Optional[Naturalness]
    hlb_value: Optional[float]
    comment: Optional[str]  # Добавить ограничения на длину?
