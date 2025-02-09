from fastapi import APIRouter


@composition_router.post("/")
async def create_user(form: RegistrationFormModel):
    return {"Hello": "World"}
