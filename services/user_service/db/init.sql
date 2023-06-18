CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

DELIMITER //
CREATE TRIGGER create_auth_entry_after_user_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO auth (user_id, username) VALUES (NEW.id, NEW.username);
END;
//
DELIMITER ;
