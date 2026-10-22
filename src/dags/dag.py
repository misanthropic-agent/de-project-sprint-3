from datetime import datetime, timedelta
from time import sleep

import pandas
from airflow import DAG
from airflow.hooks.http_hook import HttpHook
from airflow.models import TaskInstance
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

from net_funcs import (
    generate_headers,
    get_files,
    get_generated_report,
    post_generate_report,
    transform
)

path = 'data/'

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

def post_gr(ti: TaskInstance):
    task_id = post_generate_report(headers).get('task_id')
    ti.xcom_push('task_id', task_id)

def get_gr(ti: TaskInstance):
    status = ''
    while status != 'SUCCESS':
        response = get_generated_report(ti.xcom_pull(key='task_id'), headers, url=cloud_url)
        status = response['status']
        sleep(10) 
    report_id = response['data']['report_id']
    ti.xcom_push('report_id', report_id)

def task_get_fs_incr(ti: TaskInstance):
    dfs = get_files(ti.xcom_pull(key='report_id'), date=..., nick=headers['nick'], cohort=headers['cohort'], url=s3_url)
    for file_name, df in dfs:
        transformed_df = transform(df)
        transformed_df.to_csv(path + file_name)


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
    ) as dag:

    task_generate_report = PythonOperator(
        python_callable=post_gr
        )
    
    task_get_generated_report = PythonOperator(
            python_callable=get_gr
            )

    task_incr = PythonOperator(
        python_callable=task_get_fs_incr
    )

    

    

        

    post_generate_report \
        >> get_generated_report \
        >> task_get_fs_incr \
        >> []
