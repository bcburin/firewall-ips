from fastapi import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN, HTTP_501_NOT_IMPLEMENTED, HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS)

from src.common.exceptions.httpexc_provider import IHTTPExceptionProvider


class AuthException(IHTTPExceptionProvider):

    def __init__(self, message: str):
        self.message = message

    def get_http_exception(self) -> HTTPException:
        return HTTPException(status_code=HTTP_403_FORBIDDEN, detail=self.message)


class AuthenticationServiceNotLoadedException(IHTTPExceptionProvider):

    def __init__(self, message: str | None = None):
        self.message = f"Authentication service not loaded{ f': {message}' if message is not None else ''}"

    def get_http_exception(self) -> HTTPException:
        return HTTPException(status_code=HTTP_501_NOT_IMPLEMENTED, detail=self.message)


class IncorrectCredentialsException(IHTTPExceptionProvider):
    def get_http_exception(self) -> HTTPException:
        message = 'Incorrect email or password.'
        return HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=message)


class LoginTriesLimitExceeded(IHTTPExceptionProvider):
    def get_http_exception(self) -> HTTPException:
        message = "Maximum number of login tries was exceeded, resulting in account block."
        return HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS, detail=message)
