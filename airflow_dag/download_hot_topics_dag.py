from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'download_hot_topics',
    description = 'Download hot topics',
    schedule_interval = '0 0 * * *',
    start_date = datetime(2019, 9, 2),
    default_args = default_args
)

with dag:
    dummy_operator = BashOperator(
        task_id = 'download_topics',
        bash_command = 'python /scripts/download_hot_topics.py --directory /script_output'
    )