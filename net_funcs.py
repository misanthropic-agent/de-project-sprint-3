import requests
import pandas as pd
import time

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
        nick: str = 'arthur',
        cohort: str = '0',
        project: str = 'True',
        apikey: str = '5f55e6c0-e9e5-4a9c-b313-63c01fc31460',
        url: str = 'https://d5dg1j9kt695d30blp03.apigw.yandexcloud.net/generate_report'
        ) -> tuple[int, str]:

    response = requests.post(url, headers=generate_headers(nick, cohort, project, apikey))
    return response.status_code, response.json()


def get_generated_report(
        task_id: str,
        nick: str = 'arthur',
        cohort: str = '0',
        project: str = 'True',
        apikey: str = '5f55e6c0-e9e5-4a9c-b313-63c01fc31460',
        url: str = 'https://d5dg1j9kt695d30blp03.apigw.yandexcloud.net/get_report?task_id='
    ):
    response = requests.get(url + task_id, headers=generate_headers(nick, cohort, project, apikey))
    return  response.status_code, response.json()

def get_files(
        report_id: str,
        date: str ='*',
        path: str = './data/',
        nick: str = 'arthur',
        cohort: str = '0',
        url: str = 'https://storage.yandexcloud.net/s3-sprint3/cohort_$cohort/$nick/project/$report_id/$file_name'    
    ):

    files = (
    'customer_research.csv',
    'user_order_log.csv',
    'user_activity_log.csv',
    'price_log.csv',
    )

    fmt_url = url.replace('$nick', nick).replace('$cohort', cohort).replace('$report_id', report_id)

    if date != '*':
        fmt_url += f'&sdate={date}'

    for file in files:
        pd.read_csv(fmt_url.replace('$file_name', file)).to_csv(path + file)

def transform():
    ...

#_, response = post_generate_report()

task_id='MjAyNi0xMC0xOVQxMzo1NzoyOAlhcnRodXI='

#_, response = get_generated_report(response['task_id'])


report_id = 'TWpBeU5pMHhNQzB4T1ZReE16bzBNem95TmdsaGNuUm9kWEk9'

#_, response = get_generated_redocker psport(task_id)

get_files(report_id)