#!/usr/bin/env bash

set -x

docker build -t ghcr.io/mosermichael/conv_llm_html_to_markdown:latest .

if [[ $1 == "push" ]]; then
    if [[ -f ~/.github ]]; then
      source ~/.github
    fi

    add_opt=""
    if [[ $GITHUB_API_TOKEN == "" ]]; then
       echo "can't push image, without env variable GITHUB_API_TOKEN"
    fi

    echo "$GITHUB_API_TOKEN" | docker login ghcr.io -u MoserMichael --password-stdin

    docker push ghcr.io/mosermichael/conv_llm_html_to_markdown:latest
fi
