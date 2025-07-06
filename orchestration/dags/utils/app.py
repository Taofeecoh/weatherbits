import time
import logging

import awswrangler as wr
import boto3
import pandas as pd
import requests
from airflow.models import Variable



base_url = 'https://api.weatherbit.io/v2.0/forecast/agweather'
params = {
    'lat': '9.896527',  # Jos N source: maps of world
    'lon': '8.858331', # Jos E
    'key': Variable.get("WEATHERBITS_API_SECRET_KEY")
        }

# Create logger object
logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s:%(message)s"
)

my_path = "s3://tao-general-ingestion2/airflow-weatherbits-dump/"
file_path = "{}weatherbits-{}.parquet".format(my_path, time.strftime("%Y-%m-%d|%H:%M:%S"))


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


def api_to_storage(url, querystrings, s3_key):
    """
    Function to extract data from an endpoint and store json format data.
    :params url: base url of request
    :params querystrings: url endpoints
    :params file_path: path/to/filename in s3 bucket
    """
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            response = response.json()
            data = pd.json_normalize(response)
            wr.s3.to_parquet(
                df=data,
                path=file_path,
                boto3_session=boto_session(),
                dataset=False
            )
            logging.info("upload complete!")
        else:
            logging.info("Error!!!", response.text)
    except Exception as e:
        logging.info("Connection error:", e)


# def transform():
#     """
#     Function to transform json file to dataframe
#     :returns: prints completion message 
#     """
#     with open(airflow_temp_storage+'weatherbits.json') as file:
#         r_json = json.load(file)
#     response_list = r_json['data']
#     weatherbits_df = pd.DataFrame(data=response_list)
#     weatherbits_df.to_csv(airflow_temp_storage+'weatherbits.csv')
#     print("file transformation complete!")


# def s3_upload(filename, key, bucket_name):
#     hook = S3Hook("aws_weatherbits")
#     hook.load_file(filename=filename, key=key, bucket_name=bucket_name)
#     print("upload complete!")




# def to_s3():
#     """
#     Function to write DataFrame to S3 in parquet format.
#     :return: completion messsage when upload is completed successfully
#     """
#     my_path = "s3://tao-general-ingestion/airflow-weatherbits-dump/"
#     data = pd.read_csv(airflow_temp_storage+'weatherbits.csv')
#     data = pd.DataFrame(data)
#     wr.s3.to_parquet(
#         df=data,
#         path=f"{my_path}weatherbits-{time.strftime("%Y-%m-%d|%H:%M:%S")}.parquet",
#         boto3_session=boto_session(),
#         dataset=False
#     )
#     print("upload complete!")
