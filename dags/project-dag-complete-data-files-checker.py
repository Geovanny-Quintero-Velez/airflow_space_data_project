from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

default_args = {'start_date':datetime(2025,4,13) }

template_command="""

    echo '{{ds}}'

"""

with DAG(dag_id='project_dag_complete_data_files_checker',
         schedule_interval='@once',
         default_args=default_args,
         max_active_runs=1
         ) as dag:
    
    t0 = BashOperator(task_id='date_log',
                      bash_command=template_command
                      )
    
    s1 = FileSensor(task_id='NASA_data_checker',
                    filepath='/tmp/platzi_data_{{ds_nodash}}.csv',
                    poke_interval=30
                    )
    
    s2 = FileSensor(task_id='spaceX_data_checker',
                    filepath='/tmp/history.json',
                    poke_interval=30
                    )
    
    t1 = BashOperator(task_id='data_completeness_notification',
                      bash_command='echo "Data completeness verified"',
                      trigger_rule=TriggerRule.ALL_SUCCESS
                      )
    
    t0 >> [s1,s2] >> t1