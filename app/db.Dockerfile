FROM mysql:8.0.33

# copy the init.sql of each service 
COPY ./user_service/db/init.sql /docker-entrypoint-initdb.d/user_service_init.sql

CMD ["mysqld"]
