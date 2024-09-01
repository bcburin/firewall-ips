from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

from src.common.config import InjectedTokenConfig
from src.common.exceptions.auth import AuthException
from src.common.exceptions.db import NotFoundDbException, NoUpdatesProvidedDbException
from src.common.exceptions.model import DeletionOfActiveUserException
from src.models.user import UserOutModel, UserCreateModel, UserUpdateModel, User, GetAllUsers
from src.services.auth import TokenAuthManager, InjectedCurrentUser, UserLoggedIn
from src.services.database import InjectedSession

router = APIRouter(prefix='/users', tags=['Users'])

ENTITY = 'user'


@router.post(path='/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: InjectedSession, config: InjectedTokenConfig):
    user = User.authenticate(session, identifier=form_data.username, password=form_data.password)
    access_token = TokenAuthManager().generate_token(user, session, config)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/', response_model=GetAllUsers, dependencies=[UserLoggedIn])
def get_all(
        session: InjectedSession,
        page: int = Query(default=0, ge=0),
        page_size: int | None = Query(default=100, ge=0, alias='pageSize'),
        ):
    total_rows = session.query(User).count()
    users = session.query(User).order_by(User.id).offset(page * page_size).limit(page_size).all()
    return GetAllUsers(data=users, total=total_rows)


@router.get(path='/me', response_model=UserOutModel)
def get_user_me(current_user: InjectedCurrentUser):
    if not current_user:
        raise AuthException('Not Authenticated')
    return current_user


@router.get('/{id}', response_model=UserOutModel, dependencies=[UserLoggedIn])
def get_one(id: int, session: InjectedSession):
    user = session.query.get(id)
    if user is None:
        raise NotFoundDbException(ENTITY)
    return user


@router.post('/', response_model=UserOutModel, dependencies=[UserLoggedIn])
def create(item: UserCreateModel, session: InjectedSession):
    return User.create_from(item).save(session)


@router.put('/{id}', response_model=UserOutModel, dependencies=[UserLoggedIn])
def update(id: int, item: UserUpdateModel, session: InjectedSession):
    if not item.has_updates():
        raise NoUpdatesProvidedDbException(ENTITY)
    user: User = session.query(User).get(id)
    if user is None:
        raise NotFoundDbException(ENTITY)
    return user.update_from(update_model=item).update(session)


@router.put('/{id}/toggle', response_model=UserOutModel, dependencies=[UserLoggedIn])
def toggle_active(id: int, session: InjectedSession):
    user: User = session.query(User).get(id)
    if user is None:
        raise NotFoundDbException(ENTITY)
    if not user.active:
        user.login_attempts = 0
    user.active = not user.active
    return user.update(session)


@router.delete('/{id}', response_model=bool, dependencies=[UserLoggedIn])
def delete_one(id: int, session: InjectedSession):
    user = session.query(User).get(id)
    if user is None:
        raise NotFoundDbException(ENTITY)
    if user.active:
        raise DeletionOfActiveUserException(user)
    user.delete(session)
    return True
