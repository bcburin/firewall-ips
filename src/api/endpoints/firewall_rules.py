from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.common.exceptions.db import NotFoundDbException
from src.models.firewall_rule import FirewallRule, FirewallRuleOutModel
from src.services.database import get_session


router = APIRouter(prefix='/firewallRules', tags=['Firewall Rules'])

ENTITY = 'firewall rule'


@router.get('/', response_model=list[FirewallRuleOutModel])
def get_all(
        skip: int = Query(default=0, ge=0),
        limit: int | None = Query(default=100, ge=0),
        session: Session = Depends(get_session)):
    return session.query(FirewallRule).offset(skip).limit(limit)


@router.get('/{id}', response_model=FirewallRuleOutModel)
def get_by_id(id: int, session: Session = Depends(get_session)):
    fwr = session.query.get(id)
    if fwr is None:
        raise NotFoundDbException(ENTITY)
    return fwr
