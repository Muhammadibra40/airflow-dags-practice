from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'migibra678',
}

with DAG(
    dag_id='bashScriptFolder',
    description='excuting a multi-task dag through a bashScript Folder',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval= timedelta(days=1),
    template_searchpath='/root/airflow/dags/bashScripts'
) as dag:

        task_A = BashOperator(
            task_id='Task_A',  
            bash_command= 'Task_A.sh'
        )

        task_B = BashOperator(
            task_id = 'Task_B',
            bash_command= 'Task_B.sh' 
        
        )

        task_C = BashOperator(
            task_id = 'Task_C',
            bash_command = 'Task_C.sh'
        )

        task_D = BashOperator(
            task_id = 'Task_D',
            bash_command = 'Task_D.sh'
        )

        
        task_E = BashOperator(
            task_id = 'Task_E',
            bash_command = 'Task_E.sh'
        )

        task_F = BashOperator(
            task_id = 'Task_F',
            bash_command = 'Task_F.sh'
        )

        task_G = BashOperator(
            task_id = 'Task_G',
            bash_command = 'Task_G.sh'
        )

# task_A >> task_B >> task_C >> task_D >> task_E >> task_F >> task_G

# task_A >> task_B 
# task_C >> task_D >> task_E >> task_F >> task_G

task_A >> task_B >> task_E 
task_A >> task_C >> task_F
task_A >> task_D >> task_G

# task_A >> task_B >> task_E 

# task_A >> task_D >> task_G

# task_A >> task_C >> task_F


# task_A >> task_B >> task_E 
# task_A >> task_C >> task_F
# task_D >> task_G 