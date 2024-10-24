from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'migibra678',
}

with DAG(
    dag_id='multi_task_dag_four',
    description='excuting a multi-task dag for the second time',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval= timedelta(days=1)
) as dag:

        task_A = BashOperator(
            task_id='Task_A',  
            bash_command= '''
            echo Task A excuted
            for i in {1..10}:
            do
                echo Task A printing $i
            done
            
            echo Task A ended
            '''
        )

        task_B = BashOperator(
            task_id = 'Task_B',
            bash_command='''
            echo Task B excuted

            sleep 4

            echo Task B ended
            '''
        )

        task_D = BashOperator(
            task_id = 'Task_D',
            bash_command = '''
            echo Task D excuted

            sleep 4

            echo Task D ended
            '''
        )

        task_C = BashOperator(
            task_id = 'Task_C',
            bash_command = '''
            echo Task C excuted

            sleep 4

            echo Task C ended
            '''
        )

# task_A.set_downstream(task_B)

# task_A.set_downstream([task_B, task_C])

# task_D.set_upstream([task_B, task_C])

task_A >> [task_B, task_C]
[task_B, task_C] >> task_D