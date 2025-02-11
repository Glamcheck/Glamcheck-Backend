from typing import Annotated

from pydantic import BaseModel, Field

CosmeticPropertyValue = Annotated[int, Field(ge=0, le=10)]

class RangeCosmeticPropertyModel(BaseModel):
    title: str
    min_value: CosmeticPropertyValue
    max_value: CosmeticPropertyValue
