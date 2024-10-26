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

def groupby_smoker(ti):

    json_data = ti.xcom_pull(task_ids='null_removal')
    df = pd.read_json(json_data)

    grouped_df = df.groupby('smoker').agg({
        'age' : 'mean',
        'bmi' : 'mean',
        'charges' : 'mean'
    }).reset_index()

    grouped_df.to_csv('/root/airflow/dags/output/insurance_groupedBySmoker.csv', index=False)

def groupby_region(ti):

    json_data = ti.xcom_pull(task_ids='null_removal')
    df = pd.read_json(json_data)

    regionGrouped_df = df.groupby('region').agg({
        'age' : 'mean',
        'bmi' : 'mean',
        'charges' : 'mean'
    }).reset_index()

    regionGrouped_df.to_csv('/root/airflow/dags/output/insurance_groupedByRegion.csv', index=False)

# def load_data(**kwargs):

#     ti = kwargs['ti']

#     df = ti.xcom_pull(task_ids='null_removal')

#     df = pd.read_json(df)

#     df.to_csv('/root/airflow/dags/output/new_insurance.csv', index=False)

#     print(df)

#     print('Data was loaded successfully!!')



with DAG(
    'first_real_etl',
    description='making an etl',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',
    tags = ['python', 'transform', 'grouping']
) as dag:
    read_csv_file = PythonOperator(
        task_id='read_csv_file',
        python_callable=read_csv_file
    )

    remove_nulls = PythonOperator(
        task_id = 'null_removal',
        python_callable=remove_null_values
    )

    groupby_Smoker = PythonOperator(
        task_id = 'smoker_grouping',
        python_callable=groupby_smoker
    )

    groupby_Region = PythonOperator(
        task_id = 'region_grouping',
        python_callable=groupby_region
    )

read_csv_file >> remove_nulls 

remove_nulls >> [groupby_Smoker, groupby_Region]