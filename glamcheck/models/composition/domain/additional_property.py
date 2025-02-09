from pydantic import BaseModel


class AdditionalPropertyModel(BaseModel):
    title: str
    value: str
