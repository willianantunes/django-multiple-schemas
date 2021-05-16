from contextlib import contextmanager

import psycopg2

from django_multiple_schemas.support.django_helpers import getenv_or_raise_exception
from tests.support.database_utils import transform_role_config_param_details_result_dtos
from tests.support.database_utils import transform_role_dql_result_to_dtos

_system_schemas = [("pg_toast",), ("pg_catalog",), ("public",), ("information_schema",)]
_system_databases = [("postgres",), ("boss_role",)]
_system_roles = [
    ("pg_monitor",),
    ("pg_read_all_settings",),
    ("pg_read_all_stats",),
    ("pg_stat_scan_tables",),
    ("pg_read_server_files",),
    ("pg_write_server_files",),
    ("pg_execute_server_program",),
    ("pg_signal_backend",),
    # I will consider this one for the sake of simplicity
    ("boss_role",),
]
_database_standard = "postgres"
_database_dev = "db_dev"
_database_prd = "db_prd"


@contextmanager
def generate_connection(database_name):
    db_name = database_name
    user = getenv_or_raise_exception("DB_MASTER_USER")
    password = getenv_or_raise_exception("DB_MASTER_PASSWORD")
    host = getenv_or_raise_exception("DB_HOST")
    port = getenv_or_raise_exception("DB_PORT")

    connection_string = f"dbname={db_name} user={user} password={password} host={host} port={port}"
    connection = None
    try:
        connection = psycopg2.connect(connection_string)
        yield connection
    finally:
        if connection:
            connection.close()


def test_should_all_roles_receive_proper_membership_attributes():
    dql = """
        SELECT outsite_roles.rolname,
               outsite_roles.rolsuper,
               outsite_roles.rolinherit,
               outsite_roles.rolcreaterole,
               outsite_roles.rolcreatedb,
               outsite_roles.rolcanlogin,
               outsite_roles.rolconnlimit,
               outsite_roles.rolvaliduntil,
               ARRAY(SELECT inside_roles.rolname
                     FROM pg_catalog.pg_auth_members auth_members
                              JOIN pg_catalog.pg_roles inside_roles ON (auth_members.roleid = inside_roles.oid)
                     WHERE auth_members.member = outsite_roles.oid) as memberof,
               outsite_roles.rolreplication
        FROM pg_catalog.pg_roles outsite_roles
    """

    roles = [
        "role_django_multiple_schemas_dev",
        "role_jafar_dev",
        "role_iago_dev",
        "role_jasmine_dev",
        "role_django_multiple_schemas_prd",
    ]

    with generate_connection(_database_standard) as connection:
        cursor = connection.cursor()
        cursor.execute(dql)

        dtos = transform_role_dql_result_to_dtos(cursor.fetchall())

        filtered_dtos = list(filter(lambda role: role.name in roles, dtos))

        assert len(filtered_dtos) == len(roles)
        for role in filtered_dtos:
            assert role.can_create_db == True
            assert role.can_create_role == False
            assert role.can_login == True
            assert role.can_replicate == False
            assert role.connection_limit == -1
            assert role.is_inherit == True
            assert role.is_super == False
            assert len(role.subscriptions) == 0
            assert role.valid_until is None


def test_should_all_roles_be_created():
    dql_list_roles = "SELECT rolname FROM pg_roles;"

    roles = [
        ("role_django_multiple_schemas_dev",),
        ("role_jafar_dev",),
        ("role_iago_dev",),
        ("role_jasmine_dev",),
        ("role_django_multiple_schemas_prd",),
    ]

    with generate_connection(_database_standard) as connection:
        cursor = connection.cursor()
        cursor.execute(dql_list_roles)
        result = cursor.fetchall()

        assert len(result) == len(roles) + len(_system_roles)
        for role in roles:
            assert role in result


def test_should_all_roles_have_search_path_set_with_one_schema_only_db_dev():
    dql_role_details = """
        SELECT r.rolname, d.datname, rs.setconfig
        FROM pg_db_role_setting rs
                 LEFT JOIN pg_roles r ON r.oid = rs.setrole
                 LEFT JOIN pg_database d ON d.oid = rs.setdatabase
        WHERE r.rolname = %s AND d.datname = %s;
    """

    roles_and_their_databases = [
        ("role_django_multiple_schemas_dev", _database_dev),
        ("role_jafar_dev", _database_dev),
        ("role_iago_dev", _database_dev),
        ("role_jasmine_dev", _database_dev),
    ]

    roles_and_their_schemas = {
        "role_django_multiple_schemas_dev": "django_multiple_schemas_dev",
        "role_jafar_dev": "jafar_dev",
        "role_iago_dev": "iago_dev",
        "role_jasmine_dev": "jasmine_dev",
    }

    for role_setup in roles_and_their_databases:
        with generate_connection(_database_standard) as connection:
            cursor = connection.cursor()
            cursor.execute(dql_role_details, role_setup)

            dtos = transform_role_config_param_details_result_dtos(cursor.fetchall())

            assert len(dtos) == 1
            role_config_param_details = dtos[0]
            role_name = role_setup[0]
            assert role_config_param_details.name == role_name
            assert role_config_param_details.database == _database_dev
            assert len(role_config_param_details.search_path) == 1
            schema = roles_and_their_schemas[role_name]
            assert role_config_param_details.search_path["search_path"] == [schema]


def test_should_have_created_two_database():
    dql_list_all_databases = "SELECT datname FROM pg_database WHERE datistemplate = false;"

    databases = [(_database_dev,), (_database_prd,)]

    with generate_connection(_database_standard) as connection:
        cursor = connection.cursor()
        cursor.execute(dql_list_all_databases)
        result = cursor.fetchall()

        count_of_database = len(databases) + len(_system_databases)
        possible_db_created_by_pytest = (f"test_{_database_standard}",)
        if possible_db_created_by_pytest in result:
            count_of_database += 1

        assert len(result) == count_of_database
        for db in databases:
            assert db in result


def test_should_have_created_four_schemas_inside_dev_database():
    dql_list_all_schemas = "select schema_name from information_schema.schemata;"

    schemas = [("django_multiple_schemas_dev",), ("jafar_dev",), ("iago_dev",), ("jasmine_dev",)]

    with generate_connection(_database_dev) as connection:
        cursor = connection.cursor()
        cursor.execute(dql_list_all_schemas)
        result = cursor.fetchall()

        assert len(result) == len(schemas) + len(_system_schemas)
        for schema in schemas:
            assert schema in result


def test_should_have_created_1_schema_inside_prd_database():
    dql_list_all_schemas = "select schema_name from information_schema.schemata;"

    schemas = [("django_multiple_schemas_prd",)]

    with generate_connection(_database_prd) as connection:
        cursor = connection.cursor()
        cursor.execute(dql_list_all_schemas)
        result = cursor.fetchall()

        assert len(result) == len(schemas) + len(_system_schemas)
        for schema in schemas:
            assert schema in result
