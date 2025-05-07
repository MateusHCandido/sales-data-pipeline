from datetime import datetime
import os
import json
import uuid
from confluent_kafka import Consumer
import boto3
from dotenv import load_dotenv

from sales.api.entity.logger import logger



load_dotenv()

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT", "http://localhost:9000"),  
    aws_access_key_id=os.getenv("MINIO_ROOT_USER", "admin"),  
    aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD", "admin123"),  
    region_name="us-east-1",  
)

bucket_name = 'sales-data'


def generate_result_log(response, type_log):
    today_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"logs_requests_{today_date}.json"

    response_data = json.loads(response.body.decode('utf-8'))

    log = {
        "success": response_data.get("success"),
        "status_code": response.status_code,
        "data": response_data
    }

    if type_log == 'info':
        logger.info(log)
    elif type_log == 'warning':
        logger.warning(log)
    elif type_log == 'error':
        logger.error(log)

    # Send log to MinIO
    try:
        existing_data = s3.get_object(Bucket=bucket_name, Key=log_filename)
        existing_logs = json.loads(existing_data['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        existing_logs = []

    existing_logs.append(log)

    # Update log files
    s3.put_object(
        Bucket=bucket_name,
        Key=log_filename,
        Body=json.dumps(existing_logs).encode('utf-8'),
        ContentType='application/json'
    )

    print(f"Log salvo no MinIO como: {log_filename}")


def main():

    topic = 'sales-cdc-logs'
    consumer_conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'minio-cdc-logs',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])

    print(f"Consumindo mensagens do tópico: {topic}")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Erro ao consumir: {msg.error()}")
                continue

            value = msg.value().decode('utf-8')
            filename = f"{uuid.uuid4()}.json"

            s3.put_object(
                Bucket=bucket_name,
                Key=filename,
                Body=value.encode('utf-8'),
                ContentType='application/json'
            )

            print(f"Mensagem salva no MinIO como: {filename}")
    except KeyboardInterrupt:
        print("Encerrando consumo...")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
