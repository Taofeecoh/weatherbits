from datetime import datetime, timedelta

from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator
import airflow_variable as airflow_variable
from utils.app import api_to_storage


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
        python_callable=api_to_storage,
        op_kwargs={
            "endpoint": base_url,
            "params": params,
            "s3_key": file_path,
        },
        dag=dag,
    )


extract_data
