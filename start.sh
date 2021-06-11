#!/bin/bash

trap cleanup &>/proc/1/fd/1 1 2 3 6

cleanup() {
    gitlab-runner unregister --all-runners
    sleep 5
}

if [[ "$TLS_CA_CERT" ]]; then
    mkdir -p /home/gitlab-runner/.gitlab-runner/certs/
    echo "$TLS_CA_CERT" > /home/gitlab-runner/.gitlab-runner/certs/$(echo "$CI_SERVER_URL" | cut -d'/' -f3 | cut -d':' -f1).crt
fi

gitlab-runner register --non-interactive \
                       --executor=custom \
                       --builds-dir="$HOME"/builds \
                       --cache-dir="$HOME"/cache \
                       --custom-prepare-exec="$HOME"/prepare.py \
                       --custom-run-exec="$HOME"/run.py \
                       --custom-cleanup-exec="$HOME"/cleanup.py

gitlab-runner run
