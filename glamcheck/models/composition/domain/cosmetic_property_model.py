from pydantic import BaseModel, Field


class CosmeticPropertyModel(BaseModel):
    title: str
    value: int = Field(ge=0, le=10)
