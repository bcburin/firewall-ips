from abc import ABC, abstractmethod

from fastapi import HTTPException


class IHTTPExceptionProvider(Exception, ABC):

    @abstractmethod
    def get_http_exception(self) -> HTTPException:
        pass
