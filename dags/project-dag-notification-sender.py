from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.email import EmailOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
import os

default_args = {'start_date':datetime(2025,4,13) }


template_command="""

    echo '{{ds}}'

"""

# --- email information load ---

html_path = os.path.join(os.path.dirname(__file__), '../email_templates/data_ready.html')
email_receiver = os.path.join(os.path.dirname(__file__), '../secrets/email_receiver.txt')

with open(html_path, 'r') as f:
    email_html = f.read()

with open(email_receiver,'r') as file:
    recipient_email = file.read().strip()

# --- Close email info load ---

with DAG(dag_id='project_dag_notification_sender',
         schedule_interval='@once',
         default_args=default_args,
         max_active_runs=1
         ) as dag:
    
    t0 = BashOperator(task_id='date_log',
                      bash_command=template_command
                      )
    
    s1 = ExternalTaskSensor(task_id='wait_for_data_integrity_validation',
                            external_dag_id='project_dag_complete_data_files_checker',
                            external_task_id='data_completeness_notification',
                            poke_interval=30
                            )
    
    t1 = EmailOperator(task_id='send_email_to_marketing',
                       to=recipient_email,
                       subject='Airflow INFO: Both SpaceX and NASA information data are ready',
                       html_content=email_html
                       )
    
    t2 = BashOperator(task_id='send_notification',
                      bash_command='echo "Email sent successfully"',
                      trigger_rule= TriggerRule.ALL_SUCCESS
                      )
    
    e1 = BashOperator(task_id='error_notification',
                      bash_command='echo "Error sending email"',
                      trigger_rule= TriggerRule.ONE_FAILED
                      )

    t0 >> s1 >> t1 >> [t2,e1]