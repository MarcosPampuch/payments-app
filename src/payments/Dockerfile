FROM python:3.11-slim

USER root

WORKDIR /opt/payments/helper
COPY ./helper .

WORKDIR /opt/payments/
COPY ./payments .

RUN chmod +x entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/sh", "-c", "/opt/payments/entrypoint.sh"]
# ENTRYPOINT ["/bin/bash", "-c", "tail -f /dev/null"]
