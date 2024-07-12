from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.common.exceptions.db import NotFoundDbException
from src.models.firewall_rule import FirewallRule, FirewallRuleOutModel
from src.services.database import get_session, InjectedSession

router = APIRouter(prefix='/firewallRules', tags=['Firewall Rules'])

ENTITY = 'firewall rule'


@router.get('/', response_model=list[FirewallRuleOutModel])
def get_all(
        session: InjectedSession,
        skip: int = Query(default=0, ge=0),
        limit: int | None = Query(default=100, ge=0),
        ):
    return session.query(FirewallRule).offset(skip).limit(limit).all()


@router.get('/{id}', response_model=FirewallRuleOutModel)
def get_by_id(id: int, session: InjectedSession):
    fwr = session.query.get(id)
    if fwr is None:
        raise NotFoundDbException(ENTITY)
    return fwr
