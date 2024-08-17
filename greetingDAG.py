from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'greeting',
    description='A greeting DAG',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Adjusted to a more reasonable interval
)

printGreeting = BashOperator(
    task_id='print_hello',
    bash_command='echo \'Greetings, the date and time are: \'',
    dag=dag,
)

printDate = BashOperator(
    task_id='print_date',
    bash_command='date',  # Corrected the typo
    dag=dag,
)

printGreeting >> printDate
