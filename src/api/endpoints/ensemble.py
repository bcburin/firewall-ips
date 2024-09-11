from fastapi import APIRouter

from src.ai_module.pipeline import train_pipeline, create_static_rules_pipeline


router = APIRouter(prefix='/firewall-rules', tags=['Firewall Rules'])


@router.post('/train', tags=['Ensemble'])
def train_ensemble():
    train_pipeline()


@router.post('/create_static_rules', tags=['Ensemble'])
def train_ensemble():
    create_static_rules_pipeline()
