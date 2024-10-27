import pandas as pd

from airflow.utils.dates import days_ago
from airflow.models import Variable

from airflow.operators.python import BranchPythonOperator, PythonOperator

from airflow import DAG



default_args = {
    'owner' : 'migibra678'
}


def read_csv():

    df = pd.read_csv('/root/airflow/dags/datasets/car_data.csv')

    print(df)

    return df.to_json()

def determine_branch():

    needed_output = Variable.get("transform", default_var=None)

    if needed_output == 'filter_two_seaters':
        return 'filter_two_seaters_task'
    else:
        return 'filter_fwds_task'
    
def filter_two_seaters(ti):
    json_data = ti.xcom_pull(task_ids='read_csv_task')

    df = pd.read_json(json_data)

    two_seater_df = df[df['Seats'] == 2]

    ti.xcom_push(key='transform_result', value=two_seater_df.to_json())
    ti.xcom_push(key='transform_filename', value='two_seaters')

def filter_fwds(ti):
    json_data = ti.xcom_pull(task_ids='read_csv_task')

    df = pd.read_json(json_data)

    fwd_df = df[df['PowerTrain'] == 'FWD']

    ti.xcom_push(key='transform_result', value=fwd_df.to_json())
    ti.xcom_push(key='transform_filename', value='fwd')


def write_csv_result(ti):

    json_data = ti.xcom_pull(key='transform_result')
    file_name = ti.xcom_pull(key='transform_filename')

    df = pd.read_json(json_data)

    df.to_csv(f'/root/airflow/dags/output/{file_name}.csv')


with DAG(
    dag_id='branching_datapipeline',
    description='just a datapipeline with a branching approach',
    default_args = default_args,
    start_date=days_ago(1),
    schedule_interval='@once'
) as dag:
    
    read_csv_task = PythonOperator(
        task_id='read_csv_task',
        python_callable=read_csv
    )
    
    determine_choice_task = BranchPythonOperator(
        task_id='determine_choice_task',
        python_callable=determine_branch
    )
    
    filter_two_seaters_task = PythonOperator(
        task_id='filter_two_seaters_task',
        python_callable=filter_two_seaters
    )
    
    filter_fwds_task = PythonOperator(
        task_id='filter_fwds_task',
        python_callable=filter_fwds
    )

    write_csv_result_task = PythonOperator(
        task_id = 'write_csv_result_task',
        python_callable=write_csv_result,
        trigger_rule='none_failed'
    )

read_csv_task >> determine_choice_task >> [filter_two_seaters_task, filter_fwds_task] >> write_csv_result_task
