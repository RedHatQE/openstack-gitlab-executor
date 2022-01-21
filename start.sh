#!/bin/bash

trap cleanup 1 2 3 6

cleanup() {
    if [[ "$UNREGISTER_ON_EXIT" ]]; then
        gitlab-runner unregister --all-runners
    else
        gitlab-runner stop
    fi
    sleep 5
}

if [[ "$TLS_CA_CERT" ]]; then
    mkdir -p "$HOME"/.gitlab-runner/certs/
    echo "$TLS_CA_CERT" > "$HOME"/.gitlab-runner/certs/$(echo "$CI_SERVER_URL" | cut -d'/' -f3 | cut -d':' -f1).crt
fi

echo "$PRIVATE_KEY" > "$HOME"/priv_key

if [[ "$REGISTER_ON_ENTER" ]]; then
gitlab-runner register --non-interactive \
                       --executor=custom \
                       --custom-config-exec="$HOME"/config.sh \
                       --custom-prepare-exec="$HOME"/prepare.py \
                       --custom-run-exec="$HOME"/run.py \
                       --custom-cleanup-exec="$HOME"/cleanup.py
else
    gitlab-runner start
fi

if [[ "$CONCURRENT" ]]; then
    sed -i "s/concurrent = .*/concurrent = $CONCURRENT/g" "$HOME"/.gitlab-runner/config.toml
fi

gitlab-runner run
