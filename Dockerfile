FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install pygame

RUN apt-get install -y x11-apps

RUN useradd --create-home \
            --home-dir /home/user \
            --shell /bin/bash \
            user; \
    usermod -u 1001 user; \
    groupmod -g 1001 user; \
    chown 1001:1001 /home/user

COPY src /home/user/app

USER user

CMD ["python3", "/home/user/app/gui.py"]