#!/bin/bash


sleep 30

cd /opt/payments/


echo "Migrating.."
alembic upgrade head
echo "Migrations finished!"

python3 -u /opt/payments/payments_ingestion.py