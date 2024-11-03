from pydantic import BaseModel


class AdditionalProperty(BaseModel):
    title: str  # Добавить ограничения на длину?
    value: str  # Добавить ограничения на длину?
