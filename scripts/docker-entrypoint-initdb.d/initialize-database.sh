#!/bin/bash

# https://www.willianantunes.com/blog/2021/05/production-ready-shell-startup-scripts-the-set-builtin/
set -eu -o pipefail

# Interesting issues
# - https://github.com/docker-library/postgres/issues/151
# - https://github.com/docker-library/postgres/issues/175

# https://www.postgresql.org/docs/13/index.html
# https://www.postgresql.org/docs/13/sql-createschema.html
# https://www.postgresql.org/docs/13/manage-ag-createdb.html
# https://www.postgresql.org/docs/13/database-roles.html
# https://www.postgresql.org/docs/13/sql-createrole.html
# https://www.postgresql.org/docs/13/sql-grant.html
# CREATE USER is now an alias for CREATE ROLE!

echo "Your environments..."
DATABASE_DEV=db_dev
DATABASE_PRD=db_prd

echo "Each app will have your own space, which is the schema"
APP_SCHEMA_DEV_DJANGO_MULTIPLE_SCHEMAS=django_multiple_schemas_dev
APP_SCHEMA_DEV_JAFAR=jafar_dev
APP_SCHEMA_DEV_IAGO=iago_dev
APP_SCHEMA_DEV_JASMINE=jasmine_dev

echo "All PRD stuff will only be defined to django_multiple_schemas as an example"
APP_SCHEMA_PRD_DJANGO_MULTIPLE_SCHEMAS=django_multiple_schemas_prd

echo "Each app must have its own role/username"
APP_ROLE_DEV_DJANGO_MULTIPLE_SCHEMAS=role_django_multiple_schemas_dev
APP_ROLE_DEV_JAFAR=role_jafar_dev
APP_ROLE_DEV_IAGO=role_iago_dev
APP_ROLE_DEV_JASMINE=role_jasmine_dev
APP_ROLE_PRD_DJANGO_MULTIPLE_SCHEMAS=role_django_multiple_schemas_prd
echo "Defining default password for test purpose"
APP_DEFAULT_PASSWORD=please-dont-use-this-password-ever

echo "###### Creating development environment. Now loading..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE DATABASE "$DATABASE_DEV";
  \c "$DATABASE_DEV";

  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_DEV_DJANGO_MULTIPLE_SCHEMAS";
  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_DEV_JAFAR";
  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_DEV_IAGO";
  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_DEV_JASMINE";

  CREATE ROLE "$APP_ROLE_DEV_DJANGO_MULTIPLE_SCHEMAS" WITH LOGIN CREATEDB PASSWORD '$APP_DEFAULT_PASSWORD';
  GRANT ALL PRIVILEGES ON SCHEMA "$APP_SCHEMA_DEV_DJANGO_MULTIPLE_SCHEMAS" TO "$APP_ROLE_DEV_DJANGO_MULTIPLE_SCHEMAS";

  CREATE ROLE "$APP_ROLE_DEV_JAFAR" WITH LOGIN CREATEDB PASSWORD '$APP_DEFAULT_PASSWORD';
  GRANT ALL PRIVILEGES ON SCHEMA "$APP_SCHEMA_DEV_JAFAR" TO "$APP_ROLE_DEV_JAFAR";

  CREATE ROLE "$APP_ROLE_DEV_IAGO" WITH LOGIN CREATEDB PASSWORD '$APP_DEFAULT_PASSWORD';
  GRANT ALL PRIVILEGES ON SCHEMA "$APP_SCHEMA_DEV_IAGO" TO "$APP_ROLE_DEV_IAGO";

  CREATE ROLE "$APP_ROLE_DEV_JASMINE" WITH LOGIN CREATEDB PASSWORD '$APP_DEFAULT_PASSWORD';
  GRANT ALL PRIVILEGES ON SCHEMA "$APP_SCHEMA_DEV_JASMINE" TO "$APP_ROLE_DEV_JASMINE";
EOSQL

echo "###### Creating production environment. Now loading..."
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE DATABASE "$DATABASE_PRD";
  \c "$DATABASE_PRD";

  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_PRD_DJANGO_MULTIPLE_SCHEMAS";

  CREATE ROLE "$APP_ROLE_PRD_DJANGO_MULTIPLE_SCHEMAS" WITH LOGIN CREATEDB PASSWORD '$APP_DEFAULT_PASSWORD';
  GRANT ALL PRIVILEGES ON SCHEMA "$APP_SCHEMA_PRD_DJANGO_MULTIPLE_SCHEMAS" TO "$APP_ROLE_PRD_DJANGO_MULTIPLE_SCHEMAS";
EOSQL
