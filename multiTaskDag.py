from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'migibra678',
}

with DAG(
    dag_id='multi_task_dag',
    description='excuting a multi-task dag for the first time',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval= '@once'
) as dag:

        task_A = BashOperator(
            task_id='Task_A_first',  
            bash_command='echo Task A excuted'
        )

        task_B = BashOperator(
            task_id = 'Task_B_second',
            bash_command='echo Task B excuted'
        )

# task_A.set_downstream(task_B)

task_A.set_upstream(task_B)