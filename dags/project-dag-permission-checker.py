from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.trigger_rule import TriggerRule

from datetime import datetime

permission_expected_message='Permission issued'
default_args = {'start_date':datetime(2025,4,13) }

template_command="""

    echo '{{ds}}'

"""

def permission_checker(filename, **kwargs):

    print(
        f'checking file: {filename}'
        )
    with open(filename, 'r') as f:
        content = f.read().strip()

    if content == permission_expected_message:
        print('Valid permission')
        pass

    else:
        print('invalid permission')
        raise Exception("Invalid content in permission file")

with DAG(dag_id='project_dag_NASA_permission_checker',
         schedule_interval='@once',
         catchup = False,
         default_args=default_args,
         max_active_runs=1
         ) as dag:
    
    t0 = BashOperator(task_id='date_log',
                      bash_command=template_command
                      )
    
    s1 = FileSensor(task_id='permission_checker',
                    filepath='/tmp/NASApermission_{{ds_nodash}}.txt',
                    poke_interval=30
                    )
    
    t1 = PythonOperator(task_id='permission_validator',
                        python_callable=permission_checker,
                        op_kwargs={'filename': '/tmp/NASApermission_{{ds_nodash}}.txt'}
                        )
    
    t2 = BashOperator(task_id='permission_issued_notification',
                      bash_command='echo "Permission issued" ',
                      trigger_rule= TriggerRule.ALL_SUCCESS
                      )
    
    e1 = BashOperator(task_id='error_notification',
                      bash_command='echo "Error at validating permission format"',
                      trigger_rule= TriggerRule.ONE_FAILED
                      )
    
    t0 >> s1 >> t1 >> [t2, e1]