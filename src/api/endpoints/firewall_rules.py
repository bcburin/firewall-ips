from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.common.exceptions.db import NotFoundDbException, NoUpdatesProvidedDbException
from src.models.firewall_rule import FirewallRule, FirewallRuleCreateModel, FirewallRuleUpdateModel, \
    FirewallRuleOutModel
from src.services.models import FirewallRuleService
from src.services.database import get_session


router = APIRouter(prefix='/firewallRules', tags=['Firewall Rules'])

ENTITY = 'firewall rule'


@router.get('/', response_model=list[FirewallRuleOutModel])
def get_all(
        skip: int = Query(default=0, ge=0),
        limit: int | None = Query(default=100, ge=0),
        session: Session = Depends(get_session)):
    return FirewallRuleService(session=session).get_all(skip=skip, limit=limit)


@router.get('/{id}', response_model=FirewallRuleOutModel)
def get_by_id(id: int, session: Session = Depends(get_session)):
    return FirewallRuleService(session=session).get_by_id(id_value=id)


@router.post('/', response_model=FirewallRuleOutModel)
def create(item: FirewallRuleCreateModel, session: Session = Depends(get_session)):
    return FirewallRuleService(session=session).create(obj=item)


@router.put('/{id}', response_model=FirewallRuleOutModel)
def update(id: int, item: FirewallRuleUpdateModel, session: Session = Depends(get_session)):
    if not item.has_updates():
        raise NoUpdatesProvidedDbException(origin=ENTITY)
    service = FirewallRuleService(session=session)
    db_item = service.get_by_id(id_value=id)
    if not db_item:
        raise NotFoundDbException(origin=ENTITY)
    return service.update(db_obj=db_item, obj=item)


@router.delete('/{id}', response_model=FirewallRuleOutModel)
def delete(id: int, session: Session = Depends(get_session)):
    item = FirewallRuleService(session=session).remove(pk=id)
    if not item:
        raise NotFoundDbException(origin=ENTITY)
    return item


@router.delete('/', response_model=list[FirewallRuleOutModel])
def delete_multiple(ids: list[int], session: Session = Depends(get_session)):
    deleted_users = []
    for pk in ids:
        deleted_user = FirewallRuleService(session=session).remove(pk=pk)
        deleted_users.append(deleted_user)
    return deleted_users
