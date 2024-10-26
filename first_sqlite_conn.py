from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago




default_args = {
   'owner': 'migibra678'
}



with DAG(
    'sqlite_conn',
    description='Running the sqlite db',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@once',
    tags = ['sqlite', 'database', 'sql']
) as dag:

        create_table = SqliteOperator(
            task_id = 'crate_table',
            sql = r'''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    age INTEGER NOT NULL,
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''',
            
            sqlite_conn_id='sqlite_conn',
            dag=dag,
        )

create_table

