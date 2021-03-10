from dataclasses import dataclass
from typing import Any
from typing import List
from typing import Tuple


@dataclass(frozen=True)
class RoleDetails:
    name: str
    is_super: bool
    is_inherit: bool
    can_create_role: bool
    can_create_db: bool
    can_login: bool
    connection_limit: int
    valid_until: str
    subscriptions: List[str]
    can_replicate: bool


def transform_role_dql_result_to_dtos(entries: List[Tuple[Any, ...]]) -> List[RoleDetails]:
    roles = []

    for entry in entries:
        role_details = RoleDetails(*entry)
        roles.append(role_details)

    return roles
