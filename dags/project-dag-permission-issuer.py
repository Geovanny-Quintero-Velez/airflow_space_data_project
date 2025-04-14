from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime

default_args = {'start_date':datetime(2025,4,13) }


template_command="""

    echo '{{ds}}'

"""

with DAG(dag_id='project_dag_NASA_permission_issuer',
         schedule_interval='@once',
         default_args=default_args,
         max_active_runs=1
         ) as dag:
    
    t0 = BashOperator(task_id='date_log',
                      bash_command=template_command
                      )
    
    t1 = BashOperator(task_id='NASA_permission_creator',
                      bash_command='sleep 20 && echo "Permission issued" > /tmp/NASApermission_{{ds_nodash}}.txt'
                      )

    t2 = BashOperator(task_id='success_notification',
                      bash_command='echo "Successful permission generation"',
                      trigger_rule= TriggerRule.ALL_SUCCESS
                      )

    e1 = BashOperator(task_id='error_notification',
                      bash_command='echo "Error at generating the permission"',
                      trigger_rule= TriggerRule.ONE_FAILED
                      )
    
    t0 >> t1 >> [t2, e1]