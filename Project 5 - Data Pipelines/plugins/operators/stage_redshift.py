import logging

from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    ui_color = "#358140"

    @apply_defaults
    def __init__(
        self,
        # Define your operators params (with defaults) here
        # Example:
        # redshift_conn_id=your-connection-name
        redshift_conn_id="",
        aws_credentials_id="",
        table="",
        s3_bucket="",
        s3_key="",
        json_path="",
        file_type="",
        delimiter=",",
        ignore_headers=1,
        *args,
        **kwargs,
    ):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.json_path = json_path
        self.file_type = file_type
        self.aws_credentials_id = aws_credentials_id
        self.delimiter = delimiter
        self.ignore_headers = ignore_headers

    json_sql = """
        BEGIN;
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        JSON '{}'
        COMPUPDATE OFF
        COMMIT;
    """

    csv_sql = """
        BEGIN;
        COPY {}
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        IGNOREHEADER {}
        DELIMITER '{}'
        COMMIT;
    """

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        rendered_key = self.s3_key.format(**context)
        s3_path = "s3://{}/{}".format(self.s3_bucket, rendered_key)

        if self.file_type == "json":
            formatted_sql = StageToRedshiftOperator.json_copy_sql.format(
                self.table,
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.json_path,
            )
            redshift.run(formatted_sql)

        if self.file_type == "csv":
            formatted_sql = StageToRedshiftOperator.csv_copy_sql.format(
                self.table,
                s3_path,
                credentials.access_key,
                credentials.secret_key,
                self.delimiter,
            )
            redshift.run(formatted_sql)
