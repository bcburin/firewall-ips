from fastapi import APIRouter
from pydantic import BaseModel

from src.models.critical_rule import CriticalRule
from src.models.firewall_rule import FirewallRule
from src.models.user import User
from src.services.auth import UserLoggedIn
from src.services.database import InjectedSession

router = APIRouter(prefix='/dev', tags=['Development'])


class MockConfig(BaseModel):
    n_users: int | None = None
    n_critical_rules: int | None = None
    n_firewall_rules: int | None = None


@router.post('/mock', response_model=bool, dependencies=[UserLoggedIn])
def mock_data(config: MockConfig, session: InjectedSession):
    success = True
    if config.n_users is not None:
        users = [User.mock() for _ in range(config.n_users)]
        success = success and User.bulk_create(session, users, commit=False)
    if config.n_critical_rules is not None:
        critical_rules = [CriticalRule.mock() for _ in range(config.n_critical_rules)]
        success = success and CriticalRule.bulk_create(session, critical_rules, commit=False)
    if config.n_firewall_rules is not None:
        firewall_rules = [FirewallRule.mock() for _ in range(config.n_firewall_rules)]
        success = success and FirewallRule.bulk_create(session, firewall_rules, commit=False)
    session.commit()
    return success
