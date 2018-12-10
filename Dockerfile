FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install pygame

COPY src /app/src

CMD ["python3", "/app/src/gui.py"]