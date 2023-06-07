CREATE TABLE IF NOT EXISTS messages(
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vote_type TEXT,
    votes INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

DELIMITER //

CREATE TRIGGER after_message_insert
AFTER INSERT
ON messages FOR EACH ROW
BEGIN
   INSERT INTO vote(user_id, message_id, vote_type) VALUES (NEW.user_id, NEW.message_id, 'up');
END;
//

DELIMITER ;
