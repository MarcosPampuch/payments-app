import json
import random
import time
import uuid
from datetime import datetime, timezone
from kafka import KafkaProducer
import psycopg2
from os import getenv
from helper.postgres import PostgresSQL
from helper.helper import generate_payment_record
from helper.logger import logger



def main() -> None:
    """
    Generate random payment records and publish them to a Kafka topic at regular intervals.
    Fetches user and currency IDs from Postgres for realistic data generation.
    """
    try:
       
        logger.info("Connecting to Postgres...")
        pg_conn = PostgresSQL(
            dbname=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            host=getenv("DB_HOST"),
            port=getenv("DB_PORT")
        )
        
        logger.info("Fetching user IDs...")
        user_ids = pg_conn.get_user_ids()
        logger.info(f"Found {len(user_ids)} users")
        
        logger.info("Fetching currency IDs...")
        currency_ids = pg_conn.get_currency_ids()
        logger.info(f"Found {len(currency_ids)} currencies")
        
        pg_conn.close()
        
        # Connect to Kafka
        logger.info("Connecting to Kafka...")
        producer = KafkaProducer(
            bootstrap_servers=[getenv('KAFKA_BROKER')],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        logger.info(f"Starting to generate records every 2 seconds...")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                # Generate record
                record = generate_payment_record(user_ids, currency_ids)
                
                # Publish to Kafka
                producer.send(getenv('KAFKA_TOPIC'), record)
                producer.flush()
                
                logger.info(f"Record Published: {record}")
                
                # Wait 2 seconds
                time.sleep(2)
                
        except KeyboardInterrupt:
            logger.warning("\nKeyboard interrupt received. Closing connections...")
        finally:
            producer.close()
            logger.info("Kafka producer closed.")
            
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
