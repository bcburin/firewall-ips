from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.common.exceptions.db import NotFoundDbException, NoUpdatesProvidedDbException
from src.models.critical_rule import CriticalRuleCreateModel, CriticalRuleUpdateModel, \
    CriticalRuleOutModel
from src.services.models import CriticalRuleService
from src.services.database import get_session


router = APIRouter(prefix='/criticalRules', tags=['Critical Rules'])

ENTITY = 'critical rule'


@router.get('/', response_model=list[CriticalRuleOutModel])
def get_all(
        skip: int = Query(default=0, ge=0),
        limit: int | None = Query(default=100, ge=0),
        session: Session = Depends(get_session)):
    return CriticalRuleService(session=session).get_all(skip=skip, limit=limit)


@router.get('/{id}', response_model=CriticalRuleOutModel)
def get_by_id(id: int, session: Session = Depends(get_session)):
    return CriticalRuleService(session=session).get_by_id(id_value=id)


@router.post('/', response_model=CriticalRuleOutModel)
def create(item: CriticalRuleCreateModel, session: Session = Depends(get_session)):
    return CriticalRuleService(session=session).create(obj=item)


@router.put('/{id}', response_model=CriticalRuleOutModel)
def update(id: int, item: CriticalRuleUpdateModel, session: Session = Depends(get_session)):
    if not item.has_updates():
        raise NoUpdatesProvidedDbException(origin=ENTITY)
    service = CriticalRuleService(session=session)
    db_item = service.get_by_id(id_value=id)
    if not db_item:
        raise NotFoundDbException(origin=ENTITY)
    return service.update(db_obj=db_item, obj=item)


@router.delete('/{id}', response_model=CriticalRuleOutModel)
def delete(id: int, session: Session = Depends(get_session)):
    item = CriticalRuleService(session=session).remove(pk=id)
    if not item:
        raise NotFoundDbException(origin=ENTITY)
    return item


@router.delete('/', response_model=list[CriticalRuleOutModel])
def delete_multiple(ids: list[int], session: Session = Depends(get_session)):
    deleted_users = []
    for pk in ids:
        deleted_user = CriticalRuleService(session=session).remove(pk=pk)
        deleted_users.append(deleted_user)
    return deleted_users
