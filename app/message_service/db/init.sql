CREATE TABLE IF NOT EXISTS messages(
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vote_type TEXT,
    votes INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
