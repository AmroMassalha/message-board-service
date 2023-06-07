CREATE TABLE vote(
    vote_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    message_id VARCHAR(255) NOT NULL,
    vote_type ENUM('up', 'down', 'N/A') NOT NULL DEFAULT 'N/A',
    UNIQUE KEY user_message_unique (user_id, message_id)
);
