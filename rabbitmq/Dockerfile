FROM rabbitmq:3-management-alpine

RUN apk add --no-cache jq

COPY ../rabbitmq/rabbitmq.conf /etc/rabbitmq/

COPY ./services/user_service/rabbitmq/definitions.json /services/user_service/rabbitmq/definitions.json

COPY ../rabbitmq/merge_definitions.sh /merge_definitions.sh

RUN chmod +x /merge_definitions.sh
RUN /merge_definitions.sh

RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_federation_management rabbitmq_shovel_management
