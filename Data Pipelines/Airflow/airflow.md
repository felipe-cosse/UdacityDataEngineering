# Airflow

## Airflow in Docker
```shell
$ mkdir airflow-docker
```

### Download Yaml

```shell
$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.0.1/docker-compose.yaml'
```

```shell
$ mkdir ./dags ./logs ./plugins
```

```shell
$ echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

```shell
$ sudo docker-compose up airflow-init
```

```shell
$ sudo docker-compose up -d
```


### Cleaning up

```shell
$ sudo docker-compose down --volumes --rmi all
```

### Links 

https://airflow.apache.org/docs/apache-airflow/stable/macros-ref.html