CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL
);
CREATE TABLE words (
    id SERIAL PRIMARY KEY,
    word VARCHAR(255) UNIQUE NOT NULL
);
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    word_id INTEGER REFERENCES words(id),
    active BOOLEAN DEFAULT TRUE,
    player_count INTEGER DEFAULT 1,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE scores (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES games(id),
    user_id INTEGER REFERENCES users(id),
    score INTEGER DEFAULT 0
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    game_id INTEGER REFERENCES games(id),
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE game_users (
    game_id INTEGER REFERENCES games(id),
    user_id INTEGER REFERENCES users(id),
    PRIMARY KEY (game_id, user_id)
);
