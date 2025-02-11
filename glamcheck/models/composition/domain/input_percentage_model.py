from pydantic import BaseModel

from glamcheck.models.common import DecimalModel


class InputPercentageModel(BaseModel):
    low: DecimalModel
    high: DecimalModel
