import pandas as pd

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
   'owner': 'migibra678'
}

def read_csv_file():
    df = pd.read_csv('/root/airflow/dags/datasets/insurance.csv')

    print(df)
    # DataFrame type is not JSON serializable, and Airflow's default XCom backend uses JSON to serialize data.
    # Returning the df on its format will throw an error.
    return df.to_json()


def remove_null_values(**kwargs):

    ti = kwargs['ti']

    json_data = ti.xcom_pull(task_ids='read_csv_file')

    df = pd.read_json(json_data)

    df = df.dropna()

    return df.to_json()

def load_data(**kwargs):

    ti = kwargs['ti']

    df = ti.xcom_pull(task_ids='null_removal')

    df = pd.read_json(df)

    df.to_csv('/root/airflow/dags/output/new_insurance.csv', index=False)

    print(df)

    print('Data was loaded successfully!!')



with DAG(
    'simple_etl',
    description='making a simple etl',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',
    tags = ['python', 'transform', 'etl']
) as dag:
    read_csv_file = PythonOperator(
        task_id='read_csv_file',
        python_callable=read_csv_file
    )

    remove_nulls = PythonOperator(
        task_id = 'null_removal',
        python_callable=remove_null_values
    )

    load_data = PythonOperator(
        task_id = 'data_load',
        python_callable=load_data
    )

read_csv_file >> remove_nulls >> load_data
