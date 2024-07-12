from fastapi import APIRouter, Query
from sqlmodel import Session

from src.common.exceptions.db import NotFoundDbException, NoUpdatesProvidedDbException
from src.models.critical_rule import CriticalRuleCreateModel, CriticalRuleUpdateModel, \
    CriticalRuleOutModel, CriticalRule
from src.services.database import InjectedSession

router = APIRouter(prefix='/criticalRules', tags=['Critical Rules'])

ENTITY = 'critical rule'


@router.get('/', response_model=list[CriticalRuleOutModel])
def get_all(
        session: InjectedSession,
        skip: int = Query(default=0, ge=0),
        limit: int | None = Query(default=100, ge=0),
        ):
    return session.query(CriticalRule).offset(skip).limit(limit).all()


@router.get('/{id}', response_model=CriticalRuleOutModel)
def get_one(id: int, session: InjectedSession):
    cr = session.query.get(id)
    if cr is None:
        raise NotFoundDbException(ENTITY)
    return cr


@router.post('/', response_model=CriticalRuleOutModel)
def create(item: CriticalRuleCreateModel, session: InjectedSession):
    return CriticalRule.create_from(create_model=item).save(session)


@router.put('/{id}', response_model=CriticalRuleOutModel)
def update(id: int, item: CriticalRuleUpdateModel, session: InjectedSession):
    if not item.has_updates():
        raise NoUpdatesProvidedDbException(ENTITY)
    cr: CriticalRule = session.query(CriticalRule).get(id)
    if cr is None:
        raise NotFoundDbException(ENTITY)
    return cr.update_from(update_model=item).update(session)


@router.delete('/{id}', response_model=bool)
def delete_one(id: int, session: InjectedSession):
    user = session.query.get(id)
    if user is None:
        raise NotFoundDbException(ENTITY)
    user.delete(session)
    return True


@router.delete('/', response_model=bool)
def delete_multiple(ids: list[int], session: InjectedSession):
    session.execute(CriticalRule.__table__.delete().where(CriticalRule.id.in_(ids)))
    session.commit()
    return True
