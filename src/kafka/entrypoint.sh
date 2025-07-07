#!/bin/bash

/etc/kafka/docker/run &

sleep 10

echo "Kafka cluster running"
/opt/kafka/bin/kafka-topics.sh --create --topic payments-events --bootstrap-server broker:29092
echo "Topic payments-events created"



/opt/kafka/bin/kafka-topics.sh --create --topic import-payments-events --bootstrap-server broker:29092
echo "Topic import-payments-events created"


tail -f /dev/null