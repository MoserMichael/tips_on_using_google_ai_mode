#!/usr/bin/env bash


while getopts "hvf:d:" opt; do
  case ${opt} in
    h)
        docker run --rm -it ghcr.io/mosermichael/conv_llm_html_to_markdown:latest -h
        ;;
    f)
        IN_FILE=$OPTARG
        FULL_PATH=$(realpath $IN_FILE)
        DIR_PATH="${FULL_PATH%/*}"
        FILE_NAME="${FULL_PATH##*/}"

        docker run -v ${DIR_PATH}:/in_dir --rm -it ghcr.io/mosermichael/conv_llm_html_to_markdown:latest -f "/in_dir/${FILE_NAME}"
        ;;
    d)
        IN_DIR=$OPTARG
        DIR_PATH=$(realpath $IN_DIR)
        docker run -v ${DIR_PATH}:/in_dir --rm -it ghcr.io/mosermichael/conv_llm_html_to_markdown:latest -d "/in_dir"
        ;;
    v)
        set -x
    	export PS4='+(${BASH_SOURCE}:${LINENO}) '
        ;;
    *)
        echo "Invalid Option"
        Help
        ;;
   esac
done



