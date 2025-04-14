from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import os

default_args = {'start_date':datetime(2025,4,13) }
destination_path = '/tmp/history.json'

template_command="""

    echo '{{ds}}'

"""

def spaceX_data_check(filename, **kwargs):
    if not os.path.exists(filename) or os.path.getsize(filename)==0:
        raise ValueError(f'file "{filename}" is empty or does not exist')
    
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError('invalid json file')
    
    if not data:
        raise ValueError('Empty json file')
    
    print('Valid json file')

with DAG(dag_id='project_dag_spacex_API_consumer',
         schedule_interval='@once',
         default_args=default_args,
         max_active_runs=1
         ) as dag:
    
    t0 = BashOperator(task_id='date_log',
                      bash_command=template_command
                      )
    
    t1 = BashOperator(task_id='spacex_api_consumer',
                      bash_command=f'curl -o {destination_path} -L "https://api.spacexdata.com/v4/history"'
                      )
    
    t2 = PythonOperator(task_id='data_validator',
                        python_callable=spaceX_data_check,
                        op_kwargs={'filename':destination_path}
                        )
    
    t3 = BashOperator(task_id='success_notification',
                      bash_command='echo "Successful data ingestion"',
                      trigger_rule= TriggerRule.ALL_SUCCESS
                      )

    e1 = BashOperator(task_id='error_notification',
                      bash_command='echo "Error consuming data"',
                      trigger_rule= TriggerRule.ONE_FAILED
                      )
    
    t0 >> t1 >> t2 >> [t3, e1]