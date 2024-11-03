from pydantic import BaseModel, EmailStr


class LoginFormModel(BaseModel):
    email: EmailStr
    password: str
