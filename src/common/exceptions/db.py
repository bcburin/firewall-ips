from typing import Any

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from src.common.exceptions.httpexc_provider import IHTTPExceptionProvider


class DbException(IHTTPExceptionProvider):

    def __init__(self, origin: str):
        self.origin = origin

    def get_http_exception(self):
        return HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Error accessing {self.origin}')


class NotFoundDbException(DbException):

    def __init__(self, origin: str):
        super().__init__(origin=origin)

    def get_http_exception(self):
        return HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'No such {self.origin}')


class AlreadyExistsDbException(DbException):

    def __init__(self, origin: str, repeated_attribute: str | None = None, repeated_value: Any = None):
        super().__init__(origin=origin)
        self.repeated_attribute = repeated_attribute
        self.repeated_value = repeated_value

    def get_http_exception(self):
        return HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f'There is already an entry for {self.origin} with {self.repeated_attribute} as '
                   f'{self.repeated_value}'
                   if self.repeated_attribute else
                   f'There is already such an entry for {self.origin}')


class NoUpdatesProvidedDbException(DbException):

    def __init__(self, origin: str):
        super().__init__(origin=origin)

    def get_http_exception(self):
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f'No updates provided for {self.origin}')
