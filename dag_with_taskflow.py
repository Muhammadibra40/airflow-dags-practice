import time
from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from airflow.decorators import dag, task

default_args = {
    'owner' : 'migibra678' 
}

@dag(
    dag_id='dag_with_taskflow',
    description='dagging with TaskFlow!!',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@once',
    tags=['TaskFlow_api', 'Pure Python']
)
def dag_with_taskflow_api():



    @task
    def task_a():
        print("Task A excuted!")

    @task
    def task_b():
        time.sleep(5)
        print("Task B excuted!")

    @task
    def task_c():
        time.sleep(5)
        print("Task C excuted!")

    @task
    def task_d():
        time.sleep(5)
        print("Task D excuted!")

    @task
    def task_e():
        print("Task E excuted!")

    task_a() >> [task_b(), task_c(), task_d()] >> task_e()


dag_with_taskflow_api()