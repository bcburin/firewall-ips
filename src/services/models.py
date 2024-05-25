from typing import Any

import bcrypt
from sqlmodel import Session

from src.models.critical_rule import CriticalRule, CriticalRuleCreateModel, CriticalRuleUpdateModel
from src.models.firewall_rule import FirewallRule, FirewallRuleCreateModel, FirewallRuleUpdateModel
from src.models.user import UserCreateModel, User, UserUpdateModel
from src.services.database import BaseDbService, ModelType


class CriticalRuleService(BaseDbService[CriticalRule, CriticalRuleCreateModel, CriticalRuleUpdateModel]):

    def __init__(self, session: Session):
        super().__init__(model=CriticalRule, session=session)


class FirewallRuleService(BaseDbService[FirewallRule, FirewallRuleCreateModel, FirewallRuleUpdateModel]):

    def __init__(self, session: Session):
        super().__init__(model=FirewallRule, session=session)


class UserService(BaseDbService[User, UserCreateModel, UserUpdateModel]):

    def __init__(self, session: Session):
        super().__init__(model=User, session=session)

    def get_by_email(self, email: str) -> User | None:
        return self.get_by_unique_attribute(id_name='email', id_value=email)

    def get_by_username(self, username: str) -> User | None:
        return self.get_by_unique_attribute(id_name='username', id_value=username)

    def get_by_username_or_email(self, identifier: str) -> User | None:
        user = self.get_by_username(username=identifier)
        if user is not None:
            return user
        return self.get_by_email(email=identifier)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create(self, *, obj: UserCreateModel, refresh: bool = True) -> User:
        password_hash = self.hash_password(password=obj.password)
        user_data = {
            **obj.dict(),
            'password_hash': password_hash,
        }
        del user_data['password']
        db_user = User(**user_data)
        self.session.add(db_user)
        self.session.commit()
        if refresh:
            self.session.refresh(db_user)
        return db_user

    def update(self, *, db_obj: User, obj: UserUpdateModel | dict[str, Any]) -> ModelType:
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)
        if 'password' in update_data:
            password_hash = self.hash_password(password=update_data['password'])
            update_data['password_hash'] = password_hash
            del update_data['password']
        return super().update(db_obj=db_obj, obj=update_data)

    def authenticate(self, identifier: str, password: str) -> User | None:
        user = self.get_by_username_or_email(identifier=identifier)
        if user is None or not self.check_password(password=password, hashed_password=user.password_hash):
            return None
        return user
