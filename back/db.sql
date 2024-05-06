CREATE DATABASE IF NOT EXISTS musdraw;
USE musdraw;
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Words (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word VARCHAR(255) NOT NULL
);

CREATE TABLE Games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    word_id INT,
    active BOOLEAN DEFAULT TRUE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES Words(id)
);

CREATE TABLE Scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    user_id INT,
    score INT DEFAULT 0,
    FOREIGN KEY (game_id) REFERENCES Games(id),
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
