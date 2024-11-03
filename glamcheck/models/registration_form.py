from pydantic import BaseModel, EmailStr, PastDate

from .gender import Gender


class RegistrationFormModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    birth_date: PastDate
    password: str
    gender: Gender
