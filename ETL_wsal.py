from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

input_file = 'web-server-access-log.txt'
extracted_file = 'extracted-data.txt'
transformed_file = 'transformed.txt'
output_file = 'data_for_analytics.csv'

def extract(input_file, extracted_file):
    print("Inside Extract")
    with open(input_file, 'r') as infile, \
            open(extracted_file, 'w') as outfile:
        for line in infile:
            fields = line.split('#')
            if len(fields) >= 6:
                field_1 = fields[0]
                field_3 = fields[2]
                field_6 = fields[5]
                outfile.write(field_1 + ":" + field_3 + ":" + field_6 + "\n")

def transform(extracted_file, transformed_file):
    print("Inside Transform")
    with open(extracted_file, 'r') as infile, \
            open(transformed_file, 'w') as outfile:
        for line in infile:
            processed_line = line.replace(':', ',')
            outfile.write(processed_line + '\n')

def load(transformed_file, output_file):
    print("Inside Load")
    with open(transformed_file, 'r') as infile, \
            open(output_file, 'w') as outfile:
        for line in infile:
            outfile.write(line + '\n')

def check(output_file):
    print("Inside Check")
    with open(output_file, 'r') as infile:
        for line in infile:
            print(line)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ETLAirflowSecTrial',
    default_args=default_args,
    description='ETL DAG',
    schedule_interval=timedelta(days=1),
)

execute_extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    op_args=[input_file, extracted_file],
    dag=dag,
)

execute_transform = PythonOperator(
    task_id='transform',
    python_callable=transform,
    op_args=[extracted_file, transformed_file],
    dag=dag,
)

execute_load = PythonOperator(
    task_id='load',
    python_callable=load,
    op_args=[transformed_file, output_file],
    dag=dag,
)

execute_check = PythonOperator(
    task_id='check',
    python_callable=check,
    op_args=[output_file],
    dag=dag,
)

execute_extract >> execute_transform >> execute_load >> execute_check
