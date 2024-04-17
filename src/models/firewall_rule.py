from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Enum as SQLModelEnum

from src.models.enums import Action


class FirewallRule(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    src_port: int | None
    des_port: int | None
    nat_src_port: int | None
    nat_des_port: int | None
    action: Action = Field(sa_column=Column(SQLModelEnum(Action)))


if __name__ == '__main__':
    rule = FirewallRule(src_port=57222, des_port=80, action=Action.ALLOW)
    print(rule)
