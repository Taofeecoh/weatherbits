from datetime import datetime, timedelta

from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
from app import extract, to_s3, transform

base_url = "https://api.weatherbit.io/v2.0/forecast/agweather"
key = Variable.get("WEATHERBITS_API_SECRET_KEY")
lat = 9.896527  # Jos N & E source: maps of world
long = 8.858331
url = f"{base_url}?lat={lat}&lon={long}&key={key}"
airflow_temp_storage = '/opt/airflow/tmp/'


args = {
    'owner': 'Taofeecoh',
    'start_date': datetime(2025, 6, 8),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}


dag = DAG(
    dag_id='weatherbits_dag',
    default_args=args,
    schedule_interval='0 5 * * *',
    catchup=False
)

extract_data = PythonOperator(
    task_id='extract_data',
    provide_context=True,
    python_callable=extract,
    op_kwargs={"endpoint": url},
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
