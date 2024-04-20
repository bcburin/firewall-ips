from sqlmodel import Session

from src.models.critical_rule import CriticalRule, CriticalRuleCreateModel, CriticalRuleUpdateModel
from src.models.firewall_rule import FirewallRule, FirewallRuleCreateModel, FirewallRuleUpdateModel
from src.services.database import BaseDbService


class CriticalRuleService(BaseDbService[CriticalRule, CriticalRuleCreateModel, CriticalRuleUpdateModel]):

    def __init__(self, session: Session):
        super().__init__(model=CriticalRule, session=session)


class FirewallRuleService(BaseDbService[FirewallRule, FirewallRuleCreateModel, FirewallRuleUpdateModel]):

    def __init__(self, session: Session):
        super().__init__(model=FirewallRule, session=session)
