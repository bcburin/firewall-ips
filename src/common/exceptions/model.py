from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from src.common.exceptions.httpexc_provider import IHTTPExceptionProvider
from src.models.user import User


class DeletionOfActiveUserException(IHTTPExceptionProvider):
    def __init__(self, user: User):
        self.user = user
        self.message = f"Can't delete user {user.username} because the account is active. Deactivate it first"

    def get_http_exception(self) -> HTTPException:
        return HTTPException(status_code=HTTP_403_FORBIDDEN, detail=self.message)
