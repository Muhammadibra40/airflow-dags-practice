from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'migibra678',
}

def print_function():
        print("This is a print funtion")

with DAG(
    dag_id='python_excution',
    description='excuting a python code',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval= timedelta(days=1),
    tags=['python_function', 'first_time']
) as dag:

        task_python = PythonOperator(
            task_id='python_task',  
            python_callable = print_function
        )


task_python