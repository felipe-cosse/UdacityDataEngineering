import logging

from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadFactOperator(BaseOperator):

    ui_color = "#F98866"

    @apply_defaults
    def __init__(
        self,
        # Define your operators params (with defaults) here
        # Example:
        # conn_id = your-connection-name
        redshift_conn_id="",
        table="",
        load_sql_stmt="",
        *args,
        **kwargs,
    ):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.load_sql_stmt = load_sql_stmt

    insert_sql = """
        BEGIN;
        INSERT INTO {}
        {};
        COMMIT;
    """

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        formatted_sql = LoadFactOperator.insert_sql.format(
            self.table, self.load_sql_stmt
        )
        redshift.run(formatted_sql)
