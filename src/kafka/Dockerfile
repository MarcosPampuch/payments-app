FROM apache/kafka:latest

USER root

COPY ./entrypoint.sh /tmp/entrypoint.sh

RUN chmod +x /tmp/entrypoint.sh

ENTRYPOINT ["/bin/bash", "-c", "/tmp/entrypoint.sh"]
# ENTRYPOINT ["/bin/bash", "-c", "/path/to/your/script.sh && tail -f /dev/null"]
