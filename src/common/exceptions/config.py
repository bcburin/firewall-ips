from fastapi import HTTPException

from starlette.status import HTTP_501_NOT_IMPLEMENTED

from src.common.exceptions.httpexc_provider import IHTTPExceptionProvider


class ConfigurationNotLoaded(IHTTPExceptionProvider):

    def __init__(self, message: str | None = None):
        self.message = f"Configurations not loaded{ f': {message}' if message is not None else ''}"

    def get_http_exception(self) -> HTTPException:
        return HTTPException(status_code=HTTP_501_NOT_IMPLEMENTED, detail=self.message)
