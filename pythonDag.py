from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'migibra678',
}

def Task_A():
        print("Task A Completed")

def Task_B():
        print("Task B Completed")

def Task_C():
        print("Task C Completed")

def Task_D():
        print("Task D Completed")

with DAG(
    dag_id='python_multiple_tasks',
    description='excuting a multi-task dag by python operator',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval= timedelta(days=1),
    tags = ['multiple python operator']
) as dag:

        task_A = PythonOperator(
            task_id = 'task_A',  
            python_callable = Task_A
        )

        task_B = PythonOperator(
            task_id = 'task_B',
            python_callable = Task_B 
        
        )

        task_C = PythonOperator(
            task_id = 'task_C',
            python_callable = Task_C
        )

        task_D = PythonOperator(
            task_id = 'task_D',
            python_callable = Task_D
        )


task_A >> task_B >> task_C >> task_D