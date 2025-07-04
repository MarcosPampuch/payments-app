FROM python:3.11-slim

USER root

WORKDIR /opt/ui-importer/helper
COPY ./helper .

WORKDIR /opt/ui-importer
COPY ./ui-importer .

ENV PYTHONUNBUFFERED=1

RUN chmod +x entrypoint.sh
RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c", "/opt/ui-importer/entrypoint.sh"]
# ENTRYPOINT ["/bin/python3", "app.py"]
# ENTRYPOINT ["/bin/bash", "-c", "tail -f /dev/null"]
