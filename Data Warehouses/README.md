# Data Warehouse

## Postgres Pagila

```sh
docker exec -it postgres-node psql -U postgres
```

```sh
psql (13.1 (Debian 13.1-1.pgdg100+1))
Type "help" for help.

postgres=# CREATE DATABASE pagila;
postgres-# CREATE DATABASE
postgres=\q
```

```sh
cat <local-repo>/pagila-schema.sql | docker exec -i postgres-node psql -U postgres -d pagila
```

```sh
cat <local-repo>/pagila-data.sql | docker exec -i postgres psql -U postgres -d pagila
```

```sh
docker exec -it postgres-node psql -U postgres
```

```
postgres
psql (13.1 (Debian 13.1-1.pgdg100+1))
Type "help" for help.

postgres=# \c pagila
You are now connected to database "pagila" as user "postgres".
pagila=# \dt
```