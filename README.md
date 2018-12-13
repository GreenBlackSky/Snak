# Snak

## About

Game of snake, which uses ML and genetic algorithms to learn to play itself.

## Snake

Snake implemented as sliding window.

## Widgets

Some generic widgets were implemented in this project, such as button, checkbox, text input and list of strings.
Widgets can relate to each other as parent-child and pass signals and events via event loop.

## GUI

pygame is used for drawning stuff.

## Build

Run src/main.py. Path to cfg/menu.yaml can be passed as argument.

Or use docker.
In build.sh replace 1001 with you UID and GID in appropriate places and run it.

## Run

Run container with run.sh script.
It will be allowed to use your X11 socket.