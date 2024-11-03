from typing import Annotated

from fastapi import Depends

from glamcheck.models.refresh_request_body import RefreshTokenBodyModel


def get_unchecked_refresh_token(body: RefreshTokenBodyModel) -> str:
    return body.refresh_token

UncheckedRefreshToken = Annotated[str, Depends(get_unchecked_refresh_token)]


def get_valid_refresh_token(unchecked: UncheckedRefreshToken) -> str:
    return unchecked

ValidRefreshToken = Annotated[str, Depends(get_valid_refresh_token)]
