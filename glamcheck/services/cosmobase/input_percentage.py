from pydantic import BaseModel, Field


class InputPercentage(BaseModel):
    from_: float = Field(ge=0)
    to_: float = Field(le=100)
