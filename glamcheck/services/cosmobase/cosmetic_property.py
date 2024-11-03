from pydantic import BaseModel, Field


class CosmeticProperty(BaseModel):
    title: str # Добавить ограничения на длину?
    value: int = Field(ge=0, le=10)
