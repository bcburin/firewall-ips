from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

from src.common.config import InjectedTokenConfig
from src.common.exceptions.auth import IncorrectCredentialsException, AuthException
from src.models.user import UserOutModel, UserCreateModel
from src.services.auth import TokenAuthManager, InjectedCurrentUser
from src.services.database import InjectedSession
from src.services.models import UserService

router = APIRouter(prefix='/users', tags=['Users'])

ENTITY = 'user'


@router.post(path='/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: InjectedSession, config: InjectedTokenConfig):
    user = UserService(session).authenticate(identifier=form_data.username, password=form_data.password)
    if not user:
        raise IncorrectCredentialsException()
    access_token = TokenAuthManager().generate_token(user, session, config)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get(path='/me', response_model=UserOutModel)
def get_user_me(current_user: InjectedCurrentUser):
    if not current_user:
        raise AuthException('Not Authenticated')
    return current_user


@router.post('/', response_model=UserOutModel)
def create(item: UserCreateModel, session: InjectedSession):
    return UserService(session).create(obj=item)


@router.get('/', response_model=list[UserOutModel])
def get_all(
        session: InjectedSession,
        skip: int = Query(default=0, ge=0),
        limit: int | None = Query(default=100, ge=0),
        ):
    return UserService(session).get_all(skip=skip, limit=limit)
