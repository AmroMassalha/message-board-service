#!/bin/bash

for filename in "$@"
do
    if [[ $filename == *\.pem || $filename == *\.key || $filename == *\.crt || $filename == *\.cer || $filename == *\.pfx || $filename == *\.jks || $filename == *\.keystore || $filename == *\.ovpn ]]; then
        echo "Error: $filename - potentially sensitive data."
        exit 1
    fi
done
