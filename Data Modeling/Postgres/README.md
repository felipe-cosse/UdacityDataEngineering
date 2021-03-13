# Postgres

## Postgres in Docker
```shell
$ docker run --name postgres-node -d -p 5432:5432 -v /tmp/database:/var/lib/postgresql/data -e POSTGRES_PASSWORD=1234 postgres
```

```shell
$ docker stop postgres-node
```

```shell
$ docker start postgres-node
```

```shell
$ docker logs postgres-node
```

## Documentação Postgres

Review this document on PostgreSQL datatypes: https://www.postgresql.org/docs/9.5/datatype.html

Python PostgresSQL Tutorial Using Psycopg2 https://pynative.com/python-postgresql-tutorial/
