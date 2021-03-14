# Cassandra

## Cassandra in Docker
```shell
$ docker run --name cassandra-node \
  -d \
  -p 7000:7000 \
  -p 7001:7001 \
  -p 7199:7199 \
  -p 9042:9042 \
  -p 9160:9160 \
  -p 9404:9404 \ 
  -v /home/felipe/cassandra:/var/lib/cassandra \
  cassandra
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

Installing Cassandra: https://cassandra.apache.org/doc/latest/getting_started/installing.html

More documentation can be found here: https://datastax.github.io/python-driver/
