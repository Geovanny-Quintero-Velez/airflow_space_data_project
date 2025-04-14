from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime

default_args = {'start_date':datetime(2025,4,13) }

template_command="""

    echo '{{ds}}'

"""

def _generate_platzi_data(**kwargs):

    import pandas as pd

    data = pd.DataFrame({"student": ["Maria Cruz", "Daniel Crema",
    "Elon Musk", "Karol Castrejon", "Freddy Vega"],
    "timestamp": [kwargs['logical_date'],
    kwargs['logical_date'], kwargs['logical_date'], kwargs['logical_date'],
    kwargs['logical_date']]})
    data.to_csv(f"/tmp/platzi_data_{kwargs['ds_nodash']}.csv",
    header=True)

with DAG(dag_id='project_dag_NASA_data_consumer',
         schedule_interval='@once',
         catchup = False,
         default_args=default_args,
         max_active_runs=1
         ) as dag:
    
    t0 = BashOperator(task_id='date_log',
                      bash_command=template_command
                      )
    
    s1 = ExternalTaskSensor(task_id='waiting_for_permission_to_consume_data',
                            external_dag_id='project_dag_NASA_permission_checker',
                            external_task_id='permission_issued_notification',
                            poke_interval=30
                            )
    
    t1 = PythonOperator(task_id='NASA_data_consumer',
                        python_callable=_generate_platzi_data
                        )
    
    t2 = BashOperator(task_id='success_notification',
                      bash_command='echo "Successful data ingestion"',
                      trigger_rule= TriggerRule.ALL_SUCCESS
                      )

    e1 = BashOperator(task_id='error_notification',
                      bash_command='echo "Error consuming data"',
                      trigger_rule= TriggerRule.ONE_FAILED
                      )
    
    t0 >> s1 >> t1 >> [t2, e1]

