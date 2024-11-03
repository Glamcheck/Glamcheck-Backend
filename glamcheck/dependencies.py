from typing import Annotated

import structlog
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from glamcheck.settings import settings
from glamcheck.db.session import get_session
from glamcheck.services.jwt import JwtService, JwtServiceSettings

logger = structlog.get_logger()

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")
UncheckedAccessToken = Annotated[str, Depends(_oauth2_scheme)]

jwt_service = JwtService(
    settings=JwtServiceSettings.model_validate(settings.dict()),
    structlog_logger=logger,
)

def get_jwt_service() -> JwtService:
    return jwt_service

JwtServiceDep = Annotated[JwtService, Depends(get_jwt_service)]
DbSessionDep = Annotated[AsyncSession, Depends(get_session)]
