import time
from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from airflow.decorators import dag, task

default_args = {
    'owner' : 'migibra678' 
}

@dag(
    dag_id='passing_parameters_with_taskflow',
    description='dagging with TaskFlow!',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@once',
    tags=['TaskFlow_api', 'Pure Python', 'abstraction of xcom']
)
def xcom_with_taskflow_api():



    @task
    def get_order_prices():
        order_price_data = {
            'o1' : 234.45,
            'o2' : 10.00,
            'o3' : 34.77,
            'o4' : 45.66,
            'o5' : 399
        }

        return order_price_data
    # option 2: in order for any task to recieve multiple input not in a dictionary
    @task#(multiple_outputs=True)
    def compute_average(order_price_data: dict):
        total = 0
        count = 0

        for order in order_price_data:
            total += order_price_data[order]
            count += 1
        
        average = total / count
        # passing multiple output can be done by reurning a dictionary 
        # option (1,2) --> return {'total_price' : total, 'average_price' : average}
        return average

    @task
    # recieving mulitple inputs as a dictionary
    # option 1:
    # def display_result(summary_data: dict)
    # option 2:
    # 
    def display_result(average):

        # option 1:
        # total_data = summary_data['total_price']
        # average_data = summary_data['average_price']
        
        # option 2:
        # 
        print(f"The average of goods price: {average}")


    data = get_order_prices()

    average_data = compute_average(data)

    display_result(average_data)

    # receiving multiple inptus can be done by receiving a dictionary or enabling option 2
    # option 1 --> display_result(returned_dict_data)
    # option 2 --> display_result(
    #                              returned_dict_data['total_price'],
    #                              returned_dict_data['average_price']  )                                
xcom_with_taskflow_api()