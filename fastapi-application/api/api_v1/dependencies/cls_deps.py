from http.client import HTTPException
from os import access
from typing import Self, Generator, Annotated

from fastapi import (
    Request,
    HTTPException,
    status,
)
from fastapi.params import Header
from pydantic import BaseModel


class PathReaderDependency:

    def __init__(self, source: str) -> None:
        self.source = source
        self._request: Request | None = None

    def as_dependency(self, request: Request) -> Generator[Self, None, None]:
        self._request = request
        yield self
        self._request = None

    @property
    def path(self) -> str:
        if self._request is None:
            return ""
        return self._request.url.path

    def read(self, **kwargs) -> dict[str, str]:
        return {
            "source": self.source,
            "path": self.path,
            "kwargs": kwargs,
        }


path_reader = PathReaderDependency(source="abc/path/foo/bar")


class TokenData(BaseModel):
    id: int
    username: str


class TokenIntrospectResult(BaseModel):
    result: TokenData


class HeaderAccessDependency:
    def __init__(self, secret_token: str) -> None:
        self.secret_token = secret_token

    def validate(self, token: str) -> TokenIntrospectResult:
        if token != self.secret_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token is invalid",
            )
        return TokenIntrospectResult(
            result=TokenData(
                id=42,
                username="join_smit",
            )
        )

    def __call__(
        self,
        token: Annotated[
            str,
            Header(
                alias="x-access-token",
            ),
        ],
    ) -> TokenIntrospectResult:
        token_data = self.validate(token=token)
        # log.info()
        return token_data


access_required = HeaderAccessDependency(secret_token="foo-bar-fizz-buzz")
