#!/bin/bash

jq -s 'reduce .[] as $item ({}; if $item then . * $item else . end)' \
  /services/user_service/rabbitmq/definitions.json \
  > /etc/rabbitmq/definitions.json
