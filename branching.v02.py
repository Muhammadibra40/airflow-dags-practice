from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.models import Variable
from datetime import datetime


default_args={
    'owner' : 'migibra678'
}


def read_csv_file():
    # Function to read the CSV file
    pass

def remove_null_values(task_instance):
    # Function to remove null values
    pass

def determine_branch(task_instance):
    transform_action = Variable.get("transform_action")
    if transform_action.startswith("filter"):
        return transform_action
    elif transform_action == "groupby_region_smoker":
        return "groupby_region_smoker"

def filter_by_southwest(task_instance):
    # Function to filter by Southwest region
    pass

def filter_by_southeast(task_instance):
    # Function to filter by Southeast region
    pass

def filter_by_northwest(task_instance):
    # Function to filter by Northwest region
    pass

def filter_by_northeast(task_instance):
    # Function to filter by Northeast region
    pass

def groupby_region_smoker(task_instance):
    # Function to group by region and smoker
    pass

with DAG(
        dag_id='conditional_branching', 
        start_date=datetime(2023, 1, 1),
        default_args=default_args, 
        schedule_interval='@daily'
)as dag: 


    read_csv_task = PythonOperator(
        task_id='read_csv_file',
        python_callable=read_csv_file
    )
    
    remove_nulls_task = PythonOperator(
        task_id='remove_null_values',
        python_callable=remove_null_values
    )
    
    branch_task = BranchPythonOperator(
        task_id='determine_branch',
        python_callable=determine_branch
    )
    
    filter_southwest_task = PythonOperator(
        task_id='filter_by_southwest',
        python_callable=filter_by_southwest
    )
    
    filter_southeast_task = PythonOperator(
        task_id='filter_by_southeast',
        python_callable=filter_by_southeast
    )
    
    filter_northwest_task = PythonOperator(
        task_id='filter_by_northwest',
        python_callable=filter_by_northwest
    )
    
    filter_northeast_task = PythonOperator(
        task_id='filter_by_northeast',
        python_callable=filter_by_northeast
    )
    
    groupby_task = PythonOperator(
        task_id='groupby_region_smoker',
        python_callable=groupby_region_smoker
    )
    
read_csv_task >> remove_nulls_task >> branch_task >> [
                                                        filter_southwest_task, 
                                                        filter_southeast_task, 
                                                        filter_northwest_task, 
                                                        filter_northeast_task, 
                                                        groupby_task
                                                     ]
