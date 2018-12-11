FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip x11-apps && \
    pip3 install pygame pyyaml

RUN useradd --create-home \
            --home-dir /home/user \
            --shell /bin/bash \
            user; \
    usermod -u 1001 user; \
    groupmod -g 1001 user; \
    chown 1001:1001 /home/user

COPY src /home/user/app/src

COPY cfg /home/user/app/cfg

USER user

CMD ["python3", "/home/user/app/src/gui.py", "/home/user/app/cfg/menu.yaml"]