FROM mysql:8.0.33

# copy the init.sql of each service
COPY ./services/user_service/db/init.sql /docker-entrypoint-initdb.d/a_service_init.sql
COPY ./services/message_service/db/init.sql /docker-entrypoint-initdb.d/b_service_init.sql
COPY ./services/vote_service/db/init.sql /docker-entrypoint-initdb.d/c_service_init.sql

CMD ["mysqld"]
