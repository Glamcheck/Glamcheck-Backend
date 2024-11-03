from fastapi import APIRouter

from glamcheck.auth_dependencies import UncheckedRefreshToken, ValidRefreshToken
from glamcheck.dependencies import JwtServiceDep, DbSessionDep, UncheckedAccessToken
from glamcheck.models.detail_response import DetailResponseModel
from glamcheck.models.login_form import LoginFormModel
from glamcheck.models.tokens_response import TokensResponseModel

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login(form: LoginFormModel, jwt_service: JwtServiceDep, db_session: DbSessionDep) -> TokensResponseModel:
    return {"Hello": "World"}


@auth_router.post("/logout")
async def logout(access_token: UncheckedAccessToken, refresh_token: UncheckedRefreshToken, jwt_service: JwtServiceDep,
                 db_session: DbSessionDep) -> DetailResponseModel:
    return {"Hello": "World"}


@auth_router.post("/refresh")
async def refresh(refresh_token: ValidRefreshToken, jwt_service: JwtServiceDep,
                  db_session: DbSessionDep) -> TokensResponseModel:
    return {"Hello": "World"}
