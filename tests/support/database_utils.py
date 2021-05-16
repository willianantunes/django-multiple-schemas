from dataclasses import dataclass
from typing import Any
from typing import Dict
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


@dataclass(frozen=True)
class RoleConfigParamDetails:
    name: str
    database: bool
    search_path: Dict[str, List[str]]


def transform_role_config_param_details_result_dtos(entries: List[Tuple[Any, ...]]):
    roles = []

    for entry in entries:
        name = entry[0]
        db = entry[1]
        params = entry[2]

        configured_params = {}
        for param in params:
            param_name, param_values = param.split("=")
            param_values = param_values.split(",")
            configured_params[param_name] = param_values

        role_details = RoleConfigParamDetails(name, db, configured_params)
        roles.append(role_details)

    return roles
