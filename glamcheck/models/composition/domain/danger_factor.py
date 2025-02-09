from pydantic import BaseModel, Field

from .danger_factor_type import DangerFactorType


class DangerFactorModel(BaseModel):
    value: int = Field(ge=0, le=10)
    type: DangerFactorType
