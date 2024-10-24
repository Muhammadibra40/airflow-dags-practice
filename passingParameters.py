from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'migibra678',
}

def greet_someone(name):
        print(f"Hello {name}, how are you")

def greet_someone_from_city(name, city):
        print(f"Hello {name}, From {city}")


with DAG(
    dag_id='python_parameters_tasks',
    description='excuting a multi-task dag by python passable parameters functions',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval= timedelta(days=1),
    tags = ['parameters passing to funtions']
) as dag:

        task_1 = PythonOperator(
            task_id = 'greet_task',  
            python_callable = greet_someone,
            op_kwargs={'name' : 'Muhammad'}
        )

        task_2 = PythonOperator(
            task_id = 'greet_city_task',
            python_callable = greet_someone_from_city,
            op_kwargs={'name' : 'Muhammad', 'city' : 'Cairo'}
        
        )



task_1 >> task_2