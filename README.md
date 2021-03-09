# Django Multiple Schemas

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

TODO.

## Usage

TODO.

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

Then execute the command `psql -U django_multiple_schemas_dev` (check if the user matches with what is in [docker-compose.yaml](./docker-compose.yaml)) to be able to execute SQL commands direct to the database.

### Listing all the schemas

If you only make `db` service up, then if you execute `select schema_name from information_schema.schemata;` you should see the following output:

```text
    schema_name     
--------------------
 pg_toast
 pg_catalog
 public
 information_schema
(4 rows)
```
