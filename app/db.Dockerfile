FROM mysql:8.0.33

# copy the init.sql of each service 
COPY ./user_service/db/init.sql /docker-entrypoint-initdb.d/a_service_init.sql
COPY ./message_service/db/init.sql /docker-entrypoint-initdb.d/b_service_init.sql
COPY ./vote_service/db/init.sql /docker-entrypoint-initdb.d/c_service_init.sql

CMD ["mysqld"]
