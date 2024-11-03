from fastapi import APIRouter

from glamcheck.models.registration_form import RegistrationFormModel

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/")
async def create_user(form: RegistrationFormModel):
    return {"Hello": "World"}


@user_router.get("/me")
async def get_me():
    return {"Hello": "World"}


@user_router.post("/verify-email")
async def verify_email():
    return {"Hello": "World"}


@user_router.post("/reset-password")
async def start_reset_password():
    return {"Hello": "World"}


@user_router.post("/reset-password/{code}")
async def finish_reset_password():
    return {"Hello": "World"}
