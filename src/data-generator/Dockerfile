FROM python:3.11-slim

USER root

WORKDIR /opt/data-generator/helper
COPY ./helper .

WORKDIR /opt/data-generator
COPY ./data-generator .

RUN chmod +x entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c", "/opt/data-generator/entrypoint.sh"]
# ENTRYPOINT ["/bin/bash", "-c", "tail -f /dev/null"]
