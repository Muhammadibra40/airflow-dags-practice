from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow import DAG
from datetime import datetime
import random

default_args = {
    'owner' : 'migibra678'
}



def has_driving_license():
    return random.choice([True, False])

def branch(task_instance):
    if task_instance.xcom_pull(task_ids='has_driving_license'):
        return 'eligible_to_drive'
    else:
        return 'not_eligible_to_drive'

def eligible_to_drive():
    print("You can drive, you have a license.")

def not_eligible_to_drive():
    print("I'm afraid you're out of luck, you need a license to drive.")

with DAG(
    dag_id='executing_branching',
    default_args = default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily'
) as dag:
    
    task_a = PythonOperator(
        task_id='has_driving_license',
        python_callable=has_driving_license
    )
    
    task_b = BranchPythonOperator(
        task_id='branch',
        python_callable=branch
    )
    
    task_c = PythonOperator(
        task_id='eligible_to_drive',
        python_callable=eligible_to_drive
    )
    
    task_d = PythonOperator(
        task_id='not_eligible_to_drive',
        python_callable=not_eligible_to_drive
    )

task_a >> task_b >> [task_c, task_d]
