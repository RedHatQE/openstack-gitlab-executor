#!/bin/bash

trap cleanup 1 2 3 6

cleanup() {
    gitlab-runner unregister --all-runners
    sleep 5
}

if [[ "$TLS_CA_CERT" ]]; then
    mkdir -p "$HOME"/.gitlab-runner/certs/
    echo "$TLS_CA_CERT" > "$HOME"/.gitlab-runner/certs/$(echo "$CI_SERVER_URL" | cut -d'/' -f3 | cut -d':' -f1).crt
fi

echo "$PRIVATE_KEY" > "$HOME"/priv_key

gitlab-runner register --non-interactive \
                       --executor=custom \
                       --custom-prepare-exec="$HOME"/prepare.py \
                       --custom-run-exec="$HOME"/run.py \
                       --custom-cleanup-exec="$HOME"/cleanup.py

gitlab-runner run
