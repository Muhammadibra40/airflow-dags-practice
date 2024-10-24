# from airflow import DAG
# from airflow.operators.dummy import DummyOperator
# from datetime import datetime

# default_args = {
#     'owner': 'migibra678',
#     'start_date': datetime(2024, 10, 23),
# }

# dag = DAG('my_new_dag', default_args=default_args, schedule_interval='@daily')

# task = DummyOperator(task_id='dummy_task', dag=dag)


# from datetime import datetime, timedelta
# from airflow.utils.dates import days_ago
# from airflow import DAG
# from airflow.operators.bash import BashOperator

# default_args = {
#     'owner': 'migibra678',
# }

# with DAG(
#     dag_id='multi_task_dag',
#     description='executing a multi-task DAG for the first time',
#     default_args=default_args,
#     start_date=days_ago(1),
#     schedule_interval='@once'
# ) as dag:

#     task_A = BashOperator(
#         task_id='task_A_first',  # Changed from 'Task A first' to 'task_A_first'
#         bash_command='echo Task A executed'
#     )

#     task_B = BashOperator(
#         task_id='task_B_second',  # Changed from 'Task B second' to 'task_B_second'
#         bash_command='echo Task B executed'
#     )

#     task_A >> task_B  # Set task_A to run before task_B
