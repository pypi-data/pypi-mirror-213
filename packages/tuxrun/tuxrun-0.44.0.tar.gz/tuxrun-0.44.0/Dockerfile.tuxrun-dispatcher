FROM lavasoftware/lava-dispatcher:2023.03
ARG EXTRA_PACKAGES

RUN apt-get update \
    && apt-get install -q=2 \
        podman \
        ${EXTRA_PACKAGES} \
    && true

# vim: ft=dockerfile
