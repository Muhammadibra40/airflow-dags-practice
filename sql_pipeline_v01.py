from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago




default_args = {
   'owner': 'migibra678'
}



with DAG(
    'real_sql_datapipeline_v02',
    description='Running the sqlite db and running commands for the second time',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@once',
    tags = ['sqlite', 'database', 'sql', 'datapipeline']
) as dag:
        
        # I created this task to drop the table in case i did the same other three tasks to avoid duplicate data problem
        drop_table = SqliteOperator(
            task_id = 'table_drop',
            sql = r'DROP TABLE IF EXISTS users;',
            sqlite_conn_id='sqlite_conn',
            dag=dag,
        )

        create_table = SqliteOperator(
            task_id = 'create_table',
            sql = r'''
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    age INTEGER NOT NULL,
                    city VARCHR(50),
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''',
            
            sqlite_conn_id='sqlite_conn',
            dag=dag,
        )

        insert_values_1 = SqliteOperator(
                task_id = 'value_insert_1',
                sql = r'''
                INSERT INTO users(id, name, age, is_active)
                VALUES 
                        (1, 'Muhammad', 23, true),
                        (2, 'Ahmed', 22, true),
                        (3, 'mai', 24, false),
                        (4, 'kendall', 36, false);
                ''',
                sqlite_conn_id='sqlite_conn',
                dag=dag,
        )

        insert_values_2 = SqliteOperator(
                task_id = 'value_insert_2',
                sql = r'''
                INSERT INTO users(name, age)
                VALUES 
                        ('samira', 23),
                        ('yehia', 22),
                        ('khaled', 24),
                        ('shevon', 36);
                ''',
                sqlite_conn_id='sqlite_conn',
                dag=dag,
        )

        delete_from_table = SqliteOperator(
                task_id = 'values_delete',
                sql = r'DELETE FROM users WHERE is_active = 0',

                sqlite_conn_id='sqlite_conn',
                dag=dag,
        )

        update_table = SqliteOperator(
                task_id = 'update_values',
                sql  = r'''UPDATE users SET city = 'seattle';''',

                sqlite_conn_id='sqlite_conn',
                dag=dag,
        )

        show_table = SqliteOperator(
                task_id = 'showing_table',
                sql = r'''
                SELECT * 
                FROM users;
                ''',
                sqlite_conn_id='sqlite_conn',
                dag=dag,
                # Results of the excution to be on xcom
                do_xcom_push = True
        )




drop_table >> create_table >> [insert_values_1, insert_values_2] >> delete_from_table >> update_table  >> show_table 


