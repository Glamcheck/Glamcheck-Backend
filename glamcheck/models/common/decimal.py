from pydantic import BaseModel, Field


class DecimalModel(BaseModel):
    value: int = Field(description="value before division")
    divisor: int = Field(description="power of 10", ge=1)
