![alt text](images/image-1.jpg)

# Agricultural Weather Data Pipeline for Jos, Nigeria

## Overview
Brief intro to what this project does.

## Business Problem
The company relies on weather data to support agriculture-related analytics and decision-making. However, this data is only available through a third-party API (Weatherbit), and manual retrieval is inefficient, error-prone, and not scalable for daily ingestion.

Moreover, there is a growing need for infrastructure that ensures secure, automated, and traceable data delivery to a centralized storage system.


## Solution
This project implements a fully automated ETL pipeline that fetches daily agricultural weather forecasts from the Weatherbit API and stores the data in AWS S3. 

The solution is built with the following components:

- **Data Extraction**: The target Weatherbit endpoint provides 8-day agricultural weather forecasts.
- **Transformation**: Basic formatting and timestamping of the response for partitioned storage.
- **Data Load**: Stores the resulting data as Parquet in an Amazon S3 bucket.
- **Automation**: Apache Airflow orchestrates the ETL flow on a daily schedule.
- **Infrastructure as Code**: All AWS infrastructure — including IAM roles, S3 bucket, and access credentials — is provisioned securely using Terraform, with secrets managed in AWS Systems Manager Parameter Store (SSM).

This setup enables scalable, secure, and hands-free access to weather data for downstream teams such as data analysts and agronomists.


## Architecture Diagram
Illustrate:
API → Extract → Transform → Load (S3)

Terraform: IAM, S3, SSM

Airflow: Daily Orchestration

## Features
- Secure and automated weather data ingestion
- Timestamped data for historical tracking
- Airflow DAG for scheduling and monitoring
- AWS Infrastructure defined with `Terraform`
- Secrets stored in `SSM Parameter Store`

## How to Deploy
1. `terraform apply` to set up infrastructure
2. Configure Airflow environment
3. Set environment variables or mount secrets
4. Trigger DAG or wait for scheduler

## Technologies Used
- Apache Airflow
- Python
- AWS (S3, IAM, SSM)
- Terraform
- Weatherbit API

<!-- ## Future Improvements
- Add schema validation
- Introduce error handling & retries
- Extend to multiple locations or metrics -->

## Author
Taofeecoh Adesanu – Data Engineer
