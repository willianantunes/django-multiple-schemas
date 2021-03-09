#!/bin/bash

# https://www.gnu.org/software/bash/manual/bash.html#The-Set-Builtin
# -e  Exit immediately if a command exits with a non-zero status.
# -x Print commands and their arguments as they are executed.
set -x

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

# Your environments
DATABASE_DEV=db_dev
DATABASE_PRD=db_prd

# Each app will have your own space, which is the schema
APP_SCHEMA_DEV_DJANGO_MULTIPLE_SCHEMAS=django_multiple_schemas_dev
APP_SCHEMA_DEV_JAFAR=jafar_dev
APP_SCHEMA_DEV_IAGO=iago_dev
APP_SCHEMA_DEV_ALADDIN=aladdin_dev

APP_SCHEMA_PRD_DJANGO_MULTIPLE_SCHEMAS=django_multiple_schemas_prd
APP_SCHEMA_PRD_JAFAR=jafar_prd
APP_SCHEMA_PRD_IAGO=iago_prd
APP_SCHEMA_PRD_ALADDIN=aladdin_prd

# Each app must have its own role/username
APP_ROLE_DEV_DJANGO_MULTIPLE_SCHEMAS=role_django_multiple_schemas_dev
APP_ROLE_PRD_DJANGO_MULTIPLE_SCHEMAS=role_django_multiple_schemas_prd
APP_DEFAULT_PASSWORD=please-dont-use-this-password-ever

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE DATABASE "$DATABASE_DEV";
  \c "$DATABASE_DEV";

  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_DEV_DJANGO_MULTIPLE_SCHEMAS";
  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_DEV_JAFAR";
  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_DEV_IAGO";
  CREATE SCHEMA IF NOT EXISTS "$APP_SCHEMA_DEV_ALADDIN";

  CREATE ROLE "$APP_ROLE_DEV_DJANGO_MULTIPLE_SCHEMAS" WITH LOGIN CREATEDB PASSWORD '$APP_DEFAULT_PASSWORD';
  GRANT ALL PRIVILEGES ON SCHEMA "$APP_SCHEMA_DEV_DJANGO_MULTIPLE_SCHEMAS" TO "$APP_ROLE_DEV_DJANGO_MULTIPLE_SCHEMAS";
EOSQL
