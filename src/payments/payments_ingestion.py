import json
from kafka import KafkaConsumer
import psycopg2
from os import getenv
from helper.postgres import PostgresSQL
from helper.helper import open_yaml, validate_event
from helper.logger import logger


def main():
    logger.info("Connecting to Postgres...")
    pg_client = PostgresSQL(
        dbname=getenv("DB_NAME"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DB_HOST"),
        port=getenv("DB_PORT")
    )


    logger.info("Connecting to Kafka...")
    consumer = KafkaConsumer(
        getenv('KAFKA_TOPIC'),
        bootstrap_servers=[getenv('KAFKA_BROKER')],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='payments-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    payments_json_schema = open_yaml(path='./helper/message.yml')['payments']

    logger.info("Starting to consume messages from 'payments-events'")
    
    try:
        for message in consumer:
            try:
                data = json.loads(message.value)

                if not validate_event(data=data, json_schema=payments_json_schema):
                    logger.warning(f"Invalid schema: {message.value}")
                    logger.warning("Message does not correspond to the current defined schema.")
                    continue

                pg_client.upsert_transaction(data)
                logger.info(f"Upserted transaction: {data['transaction_id']}")

            except Exception as e:
                logger.error(f"Error ingesting record: {e}")
                continue
            
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Closing Kafka consumer...")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed.")
        pg_client.close()
        logger.info("Postgres client closed.")

if __name__ == '__main__':
    main()