from pydantic import BaseModel


class DetailResponseModel(BaseModel):
    detail: str
