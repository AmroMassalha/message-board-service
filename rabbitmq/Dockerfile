FROM rabbitmq:3-management-alpine

RUN apk add --no-cache jq

COPY ../rabbitmq/rabbitmq.conf /etc/rabbitmq/

RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_federation_management rabbitmq_shovel_management
