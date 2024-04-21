from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from src.common.exceptions.httpexc_provider import IHTTPExceptionProvider


class AuthException(IHTTPExceptionProvider):

    def __init__(self, message: str):
        self.message = message

    def get_http_exception(self) -> HTTPException:
        return HTTPException(status_code=HTTP_403_FORBIDDEN, detail=self.message)