from fastapi import APIRouter, Query

from src.common.exceptions.db import NotFoundDbException
from src.models.firewall_rule import FirewallRule, FirewallRuleOutModel, GetAllFirewallRules
from src.services.database import InjectedSession

router = APIRouter(prefix='/firewall-rules', tags=['Firewall Rules'])

ENTITY = 'firewall rule'


@router.get('/', response_model=GetAllFirewallRules)
def get_all(
        session: InjectedSession,
        page: int = Query(default=0, ge=0),
        page_size: int | None = Query(default=100, ge=0, alias='pageSize'),
        ):
    total_rows = session.query(FirewallRule).count()
    fwrs: list[FirewallRuleOutModel] = (session.query(FirewallRule).order_by(FirewallRule.id)
                                       .offset(page * page_size).limit(page_size).all())
    return GetAllFirewallRules(data=fwrs, total=total_rows)


@router.get('/{id}', response_model=FirewallRuleOutModel)
def get_by_id(id: int, session: InjectedSession):
    fwr = session.query.get(id)
    if fwr is None:
        raise NotFoundDbException(ENTITY)
    return fwr
