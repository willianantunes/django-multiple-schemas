# Django Multiple Schemas

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=willianantunes_django-multiple-schemas&metric=coverage)](https://sonarcloud.io/dashboard?id=willianantunes_django-multiple-schemas)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=willianantunes_django-multiple-schemas&metric=ncloc)](https://sonarcloud.io/dashboard?id=willianantunes_django-multiple-schemas)

Here you'll find an honest project that shows how to use schema with Django. It has a script that creates all the scenario the project needs in PostgreSQL, it even has tests to guarantee that it is created as expected. Check more details below!

## Why this project?

If you are in a scenario where there are many applications using the same database machine, it's advisable to create one single database, let's say `db_production`, and then separate each application by its own schema (we can understand it as a folder). This is quite important because if you are using a CDC (Change Database Capture) solution like [Amazon DMS](https://aws.amazon.com/dms/), it consumes an entire session (know more about it [here](https://aws.amazon.com/blogs/database/analyzing-amazon-rds-database-workload-with-performance-insights/)) per database, which is an quite expensive resource. 

Let's say you have three Apps and each one has its own database. If your company needs data from these three databases, then three sessions will be consumed. Now if you're using schemas, only one. To illustrate:

![An image which shows all the database's objects](./docs/database-vs-schemas.png "All schemas/folders created")

## Some basic details

You can check it out consulting [initialize-database.sh](./scripts/docker-entrypoint-initdb.d/initialize-database.sh) file.

I created a test script where it guarantees the script executed as expected. Check [test_initialize_database.py](./tests/integration/scripts/docker-entrypoint-initdb.d/test_initialize_database.py) to know more. Great place of reference [here](https://github.com/psycopg/psycopg2/tree/master/tests). 

The result is like the following (it may be outdated):

![An image which shows all the database's objects](./docs/all-schemas-and-tables-inside-schema-dev.png "All schemas/folders created")

## Development

### Updating pipenv dependencies

If you update Pipfile, you can issue the following command to refresh your lock file:

    docker-compose run remote-interpreter pipenv update

## Playing with PostgreSQL

First execute the following:

    docker-compose up -d db

When it's UP, enter the container through the command:

    docker exec -it django-multiple-schemas_db_1 bash

You can do this as well:

    docker-compose exec db bash

We're accessing through `bash`, but you are able to access `psql` directly.

Then execute the command `psql -U boss_role` (check if the user matches with what is in [docker-compose.yaml](./docker-compose.yaml)) to be able to execute SQL commands direct to the database.

### Listing all the schemas

Sample output of the command `select schema_name from information_schema.schemata;`:

```text
    schema_name     
--------------------
 pg_toast
 pg_catalog
 public
 information_schema
(4 rows)
```

### Listing all database

Sample output of the command `SELECT datname FROM pg_database WHERE datistemplate = false;`:

```text
           datname           
-----------------------------
 postgres
 django_multiple_schemas_dev
(2 rows)
```
