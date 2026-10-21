from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.models import TaskInstance
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from time import sleep
import pandas
from datetime import datetime, timedelta
from net_funcs import (
    generate_headers,
    get_files,
    post_generate_report,
    get_generated_report
)

files = (
    'customer_research.csv',
    'user_order_log.csv',
    'user_activity_log.csv',
    'price_log.csv',
    )

cloud_url = 'https://d5dg1j9kt695d30blp03.apigw.yandexcloud.net'
s3_url = 'https://storage.yandexcloud.net/s3-sprint3/cohort_$cohort/$nick/project/$report_id/$file_name' 
pg_conn = 'pg_conn'

headers = generate_headers(
    nick='defautl',
    cohort='1',
    project='True',
    apikey='5f55e6c0-e9e5-4a9c-b313-63c01fc31460'
)

def task_post_gr(ti: TaskInstance):
    task_id = post_generate_report(headers).get('task_id')
    ti.xcom_push('task_id', task_id)

def task_get_gr(ti: TaskInstance):
    status = ''
    while status != 'SUCCESS':
        response = get_generated_report(ti.xcom_pull(key='task_id'), headers, url=cloud_url)
        status = response['status']
        sleep(10) 
    report_id = response['data']['report_id']
    ti.xcom_push('report_id', report_id)

def download_fs_incr(ti: TaskInstance):
    get_files(ti.xcom_pull(key='report_id'), )

args = {
    "owner": "student",
    'email': ['student@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

date = '{{ ds }}'

with DAG \
    (
        'sales_mart',
        default_args=args,
        catchup=True,
        start_date=datetime.today() - timedelta(days=7),
        end_date=datetime.today() - timedelta(days=1),
    ):
