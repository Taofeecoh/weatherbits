import json
import os
import time

import awswrangler as wr
import boto3
import pandas as pd
import requests
from airflow.hooks.S3_hook import S3Hook
from airflow.models import Variable

base_url = "https://api.weatherbit.io/v2.0/forecast/agweather"
key = Variable.get("WEATHERBITS_API_SECRET_KEY")
lat = 9.896527  # Jos N & E source: maps of world
long = 8.858331
url = f"{base_url}?lat={lat}&lon={long}&key={key}"
airflow_temp_storage = '/opt/airflow/tmp'


# conn = Connection(
#     conn_id="aws_weatherbitsToS3",
#     conn_type="aws",
#     login=Variable.get("AIRFLOW_AWS_KEY_ID"),
#     password=Variable.get("AIRFLOW_AWS_SECRET_KEY"),
#     extra={
#         "region_name": "eu-west-1",
#     }
# )


def extract(endpoint):
    r = requests.get(endpoint)
    if r.status_code == 200:
        r = r.json()
    os.makedirs(airflow_temp_storage, exist_ok=True)
    with open(airflow_temp_storage+'/weatherbits.json', 'w') as r_json:
        json.dump(r, r_json)
    print("json file saved to path successfully!")


def transform():
    with open(airflow_temp_storage+'/weatherbits.json') as file:
        r_json = json.load(file)
    response_list = r_json['data']
    weatherbits_df = pd.DataFrame(data=response_list)
    weatherbits_df.to_csv(airflow_temp_storage+'/weatherbits.csv')
    print("file transformation complete!")


def s3_upload(filename, key, bucket_name):
    hook = S3Hook("aws_weatherbits")
    hook.load_file(filename=filename, key=key, bucket_name=bucket_name)
    print("upload complete!")


def boto_session():
    """
    Function to create a boto3 session.
    :return: A boto3 session object.
    """

    session = boto3.Session(
        aws_access_key_id=Variable.get("AIRFLOW_AWS_KEY_ID"),
        aws_secret_access_key=Variable.get("AIRFLOW_AWS_SECRET_KEY"),
        region_name="eu-west-1"
    )
    return session


def to_s3():
    """
    Function to write DataFrame to S3 in parquet and csv formats.
    :return: completion messsage
    """
    my_path = "s3://tao-weatherbits-ingestion/airflow_dump/"
    data = pd.read_csv(airflow_temp_storage+'/weatherbits.csv')
    data = pd.DataFrame(data)
    wr.s3.to_parquet(
        df=data,
        path=f"{my_path}weatherbits-{time.strftime("%Y-%m-%d")}.parquet",
        boto3_session=boto_session(),
        dataset=False
    )
    print("upload complete!")
