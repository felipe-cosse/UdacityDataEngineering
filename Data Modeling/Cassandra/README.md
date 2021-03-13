# Cassandra

## Cassandra in Docker
```shell
$ docker run --name cassandra-node -d -p 9842:9842 -v /home/felipe/cassandra:/var/lib/cassandra cassandra
```

```shell
$ docker stop cassandra-node
```

```shell
$ docker start cassandra-node
```

```shell
$ docker logs cassandra-node
```

### Connect with Cassandra client (cqlsh)

```shell
$ docker exec -it cassandra-node cqlsh
```

## Documentação Cassandra

Cassandra-docker README: https://github.com/GoogleCloudPlatform/cassandra-docker/blob/master/3/README.md
