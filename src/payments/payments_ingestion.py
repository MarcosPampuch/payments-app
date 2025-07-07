import json
from kafka import KafkaConsumer
from os import getenv
from helper.postgres import PostgresSQL
from helper.helper import open_yaml, validate_payments_event, format_imported_payment
from helper.logger import logger


def main() -> None:
    """
    Consume messages from a Kafka topic, validate them against a schema, and upsert valid records into Postgres.
    Handles errors gracefully and logs all major events.
    """
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
        bootstrap_servers=getenv('KAFKA_BROKER'),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='payments-group',
        value_deserializer=lambda x: x.decode('utf-8')
    )

    payments_json_schema = open_yaml(path='./helper/message.yml')['payments']

    consumer.subscribe([getenv('KAFKA_PAYMENTS_TOPIC'),getenv('KAFKA_IMPORTS_TOPIC')])
    logger.info("Starting to consume messages from 'payments-events' and 'import-payments-events'")
    
    try:
        for message in consumer:

            try:
                data = json.loads(message.value)
                if message.topic == 'payments-events':

                    if not validate_payments_event(data=data, json_schema=payments_json_schema):
                        logger.warning(f"Invalid schema: {message.value}")
                        logger.warning("Message does not correspond to the current defined schema.")
                        continue

                    pg_client.upsert_transaction(data)
                    logger.info(f"Upserted transaction: {data['transaction_id']}")
                
                elif message.topic == 'import-payments-events':
                    formated_json = format_imported_payment(data=data, postgres_client=pg_client)

                    if not formated_json:
                        logger.warning(f"Could not parse the imported record {data}")
                        continue

                    pg_client.upsert_transaction(formated_json,imported_transaction=True)
                    logger.info(f"Transaction inserted from CSV file {data['source_file']}")

            except Exception as e:
                logger.error(f"Error {e} while parsing or inserting message {data}")
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