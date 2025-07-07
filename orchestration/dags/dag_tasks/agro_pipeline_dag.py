import time
from datetime import datetime, timedelta

from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator
from dag_tasks import airflow_variable
from utils.app import api_to_storage


airflow_vars = airflow_variable

my_path = "s3://tao-general-ingestion2/airflow-weatherbits-dump/"
file_path = "{}weatherbits-{}.parquet".format(my_path, time.strftime("%Y-%m-%d|%H:%M:%S"))

base_url = 'https://api.weatherbit.io/v2.0/forecast/agweather' 
params = {
    'lat': '9.896527',  # Jos N source: maps of world
    'lon': '8.858331', # Jos E
    'key': Variable.get("WEATHERBITS_API_SECRET_KEY")
        }


default_args = {
    'owner': 'Taofeecoh',
    'start_date': datetime(2025, 6, 8),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}


with DAG(
    dag_id='weatherbits_dag',
    default_args=default_args,
    schedule_interval='0 5 * * *',
    catchup=False
) as dag:

    extract_to_s3 = PythonOperator(
        task_id='extract_load',
        provide_context=True,
        python_callable=api_to_storage,
        op_args=[base_url, params, file_path],
        dag=dag,
    )


extract_to_s3
