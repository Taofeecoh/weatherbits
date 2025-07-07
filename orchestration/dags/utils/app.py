import logging

import awswrangler as wr
import boto3
import pandas as pd
import requests
from airflow.models import Variable


# Create logger object
logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format="%(levelname)s:%(asctime)s:%(message)s"
)


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


def api_to_storage(
        url: str,
        querystrings: dict,
        s3_key: str,
        headers: dict | None = None
        ):
    """
    Function to extract data from an endpoint and store json format data.
    :params url: base url of request
    :params querystrings: url endpoints
    :params s3_key: path/to/filename in s3 bucket
    """
    try:
        response = requests.get(url, params=querystrings, headers=headers)
        if response.status_code == 200:
            response = response.json()
            data = pd.json_normalize(response)
            wr.s3.to_parquet(
                df=data,
                path=s3_key,
                boto3_session=boto_session(),
                dataset=False
            )
            logging.info("upload complete!")
        else:
            logging.info("Error!!!", response.text)
    except Exception as e:
        logging.info("Connection error:", e)
