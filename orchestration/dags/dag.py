from datetime import datetime, timedelta

from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
import airflow_variable
from utils.app import extract, to_s3, transform



airflow_vars = airflow_variable

args = {
    'owner': 'Taofeecoh',
    'start_date': datetime(2025, 6, 8),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}


with DAG(
    dag_id='weatherbits_dag',
    default_args=args,
    schedule_interval='0 5 * * *',
    catchup=False
) as dag:

    extract_data = PythonOperator(
        task_id='extract_data',
        provide_context=True,
        python_callable=extract,
        dag=dag,
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform,
        dag=dag,
    )

    load_to_s3 = PythonOperator(
        task_id="load_to_s3",
        python_callable=to_s3,
        dag=dag
    )

extract_data >> transform_data >> load_to_s3
