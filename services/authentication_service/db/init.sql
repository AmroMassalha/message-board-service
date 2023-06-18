CREATE TABLE auth (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    username VARCHAR(255),
    password_hash VARCHAR(255),
    registered_at TIMESTAMP,
    last_login TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
