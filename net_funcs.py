import requests
import pandas as pd
import io
from collections.abc import Generator

def generate_headers(
    nick,
    cohort,
    project,
    apikey
    ):
    return {
     
        'X-Nickname': nick,
        'X-Cohort': cohort,
        'X-Project': project,
        'X-API-KEY': apikey
    }

def post_generate_report(
        headers: dict,
        url: str = 'https://d5dg1j9kt695d30blp03.apigw.yandexcloud.net'
        ) -> tuple[int, str]:

    response = requests.post(url + '/generate_report', headers=headers)
    return response.json()


def get_generated_report(
        task_id: str,
        headers: dict,
        url: str = 'https://d5dg1j9kt695d30blp03.apigw.yandexcloud.net'
    ):
    response = requests.get(url + '/get_report?task_id=' + task_id, headers=headers)
    return  response.json()

def get_files(
        report_id: str,
        date: str ='',
        nick: str = 'arthur',
        cohort: str = '0',
        files: str = (
            'customer_research.csv',
            'user_order_log.csv',
            'user_activity_log.csv',
            'price_log.csv',
        ),
        url: str = 'https://storage.yandexcloud.net/s3-sprint3/cohort_$cohort/$nick/project/$report_id/$file_name'    
    ) -> Generator:

    fmt_url = url.replace('$nick', nick).replace('$cohort', cohort).replace('$report_id', report_id)

    if date != '':
        fmt_url += f'&date={date}'


    for file in files:
        df = pd.read_csv(fmt_url.replace('$file_name', file))
        yield file, df

        

def transform(df: pd.DataFrame):
    if 'status' not in df.columns:
        df['status'] = 'shipped'
    df = df.drop('id', axis=1)
    df = df.drop_duplicates(['uniq_id'])
    return df