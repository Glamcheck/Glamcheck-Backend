from pydantic import BaseModel

from glamcheck.models.common import DecimalModel


class RangeAdditionalPropertyModel(BaseModel):
    title: str
    min_value: DecimalModel
    max_value: DecimalModel
